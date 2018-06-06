#!/usr/bin/env python
# Written By: sudotina

import os, sys, subprocess, boto3, json
from pyslack import SlackClient

def get_secret():
    secret_name = "<whateverthenameis>"
    endpoint_url = "https://amazonaws's secretsmanager URL"
    region_name = "your-region-3"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url)

    get_secret_value_response = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])
    return get_secret_value_response['variable_name_from_json^']

# Main
slack_username = "whatever your username is"
slack_api_key = get_secret()
slack_channel = "#whatever your slack channel is"
command = [ "clamscan", "-r", "--bell", "-i", "directory to scan/"  ]

print "Running ClamAV..."
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

sys.stdout.flush()
for line in iter(p.stdout.readline, b''):
    sys.stdout.flush()
    print line
    if 'Infected files:' in line:
        l = list(line.rstrip().split(' '))
        if l[-1] != "0":
            slack_client = SlackClient(slack_api_key)
            slack_message = ":pill: Infected file(s) found scanning <whateverlocation>! See build output for details!"
            slack_client.chat_post_message(slack_channel, slack_message, username=slack_username)
	    sys.exit(1)

