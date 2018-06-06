#!/usr/bin/env python
# Written By: sudotina

import requests
import datetime
import time


while True:
    api_url = "https://apiURLThatReturnsJson/"
    before_time = datetime.datetime.now()
    response = requests.get(api_url)
    current_time = datetime.datetime.now()

    data = response.json()
    unix_time = int(time.time())
    updated_at = datetime.datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

    quote = (current_time - updated_at).total_seconds()
    request = (current_time - before_time).total_seconds()

    print 'latency {} {} between last time object was "updated_at" and current time'.format(unix_time, quote)
    print "latency {} {} - how long the API request took".format(unix_time, request)
    time.sleep(2)
