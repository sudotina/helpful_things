#!/usr/bin/env python
# Written By: sudotina

import botocore, sys, argparse, boto3, datetime
from collections import defaultdict

profiles = ['list of accepted aws cred profiles']
profile = ''

parser = argparse.ArgumentParser(description='Get the longest running aws instances per profile')
parser.add_argument('--profile', action="store", dest='profile', default=0)
args = parser.parse_args()
if args.profile in profiles:
  profile = args.profile

#Main
ec2_no_name = []
name_time = {}
todays_date = datetime.datetime.now()

try:
    session = boto3.session.Session(profile_name=profile)
except:
    sys.exit('AWS Login Expired: Please renew creds.')

ec2 = session.resource('ec2')
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for instance in running_instances:
    instance_name = ''

    try:
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]
      except:
          ec2_no_name.append(instance.id)
          continue

    if instance_name.isspace():
        ec2_no_name.append(instance.id)
        continue

    if not instance_name: # not sure about these ifs.  I think this was me being hasty. Revisit if using.
        ec2_no_name.append(instance.id)
        continue

    name_time[instance_name] = instance.launch_time

for key, value in sorted(name_time.iteritems(), key=lambda (k,v): (v,k))[:5]:
    delta = str(todays_date.date() - value.date())
    print "{} has been up for {}".format(key, delta.split(',')[0])

