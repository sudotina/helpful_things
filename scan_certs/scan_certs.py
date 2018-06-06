#!/usr/bin/env python
# Written by: sudotina

from __future__ import print_function
from datetime import datetime, timedelta
from pyslack import SlackClient
import os, fcntl, sys, re, OpenSSL

slack_username = "herpyderpy"
slack_api_key = "whateveritmightbeforyou"
slack_channel = "#cert-watch-2020"

f = open('/var/run/scan_certs.py', 'w')
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    sys.exit('scancerts.py process is already running.')

def extract_certs(pillar_filelist):
    pem_filename_sub_exp = {}

    for pillar_f in pillar_filelist:
        with open(pillar_f, 'r') as inputf:
            p = re.compile('-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----\n', re.S)
            for result in p.findall(inputf.read()):
                pem_filename_sub_exp[pillar_f]= extract_pem(result.replace('  ',''))

    return pem_filename_sub_exp


def extract_pem(cert_string):
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_string)
    sub_expire = [cert.get_subject(), datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')]

    return sub_expire

# Main
salt_root = "/salt/"
pillar_filelist=[]

for root, dirs, files in os.walk(salt_root):
    for f in files:
        if "/pillar/" in root:
            pillar_filelist.append(os.path.join(root,f))

report_data = extract_certs(pillar_filelist)

for entry in report_data:
    slack_client = SlackClient(slack_api_key)
    slack_message = ""
    subject = report_data[entry][0]
    expire_after = report_data[entry][1]

    if (expire_after - timedelta(days=30)) < datetime.now():
        slack_message = "*ACTION REQUIRED:* A certificate found in `{}`, with a subject of `{}`, is expired/will expire on *{}*.".format(entry, subject, expire_after)
    elif (expire_after - timedelta(days=60)) < datetime.now():
        slack_message = "*Warning:* A certificate found in `{}`, with a subject of `{}`, will expire on *{}*.".format(entry, subject, expire_after)
    if slack_message:
        slack_client.chat_post_message(slack_channel, slack_message, username=slack_username)
