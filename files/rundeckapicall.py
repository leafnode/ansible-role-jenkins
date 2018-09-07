#!/usr/bin/python

import os
import sys
import time
import httplib
import urllib
import json
import argparse
from pprint import pprint
from rundeck.client import Rundeck
import sys

def main():
    parser = argparse.ArgumentParser(description='Call Rundeck API')
    parser.add_argument('--token', help='Rundeck access token', default=os.environ.get('RUNDECK_TOKEN', None))
    parser.add_argument('--host', help='Rundeck hostname', default=os.environ.get('RUNDECK_HOST', None))
    parser.add_argument('command', nargs='+', help='Command to run')
    args = parser.parse_args()

    if args.token is None or args.host is None:
        print 'Token or host is not set. Use arguments or env vars'
        parser.print_usage()
        sys.exit(1)


    rd = Rundeck(args.host, port=80, api_token=args.token)

    if args.command[0] == 'list':
        list_jobs(args.host, args.token, args.command[1], args.command[2])
    elif args.command[0] == 'wait':
        wait_for_idle(args.host, args.token, args.command[1])
    elif args.command[0] == 'stop':
        stop_scheduler(args.host, args.token, args.command[1], args.command[2])
    elif args.command[0] == 'start':
        start_scheduler(args.host, args.token, args.command[1], args.command[2])
    elif args.command[0] == 'count-disabled':
        count_disabled(args.host, args.token, rd, args.command[1], args.command[2])

def list_jobs(host, token, project, group):
    print filter_jobs(host, token, project, group)

def count_disabled(host, token, rd, project, group):
    from pprint import pprint
    rd = Rundeck(host, port=80, api_token=token)
    jobs = filter(lambda x: x['group']==group, rd.list_jobs(project))
    print len(filter(lambda x: get_job_metadata(host, token, x['id'])['scheduleEnabled']==False, jobs ))

def filter_jobs(host, token, project, group):
    rd = Rundeck(host, port=80, api_token=token)
    jobs = filter(lambda x: x['group']==group, rd.list_jobs(project))
    return ','.join(map(lambda x: x['id'], jobs))

def wait_for_idle(host, token, project):
    while len(list_running(host, token, project)) > 0:
        time.sleep(1)

def list_running(host, token, project):
    return apicall(host, token, 'project/'+project+'/executions/running', 'GET')['executions']

def stop_scheduler(host, token, project, group):
    jobs = filter_jobs(host, token, project, group)
    url = "jobs/schedule/disable"
    data = { "idlist": jobs }
    apicall(host, token, url, 'POST', data)

def start_scheduler(host, token, project, group):
    jobs = filter_jobs(host, token, project, group)
    url = "jobs/schedule/enable"
    data = { "idlist": jobs }
    apicall(host, token, url, 'POST', data)

def get_job_metadata(host, token, id):
    return apicall(host, token, 'job/'+id+'/info', 'GET')

def apicall(host, token, url, method = 'POST', data = None):
    headers = {"X-Rundeck-Auth-Token" : token, 'Accept':'application/json' }
    conn = httplib.HTTPSConnection(host+':443')
    if (data):
        data = '?'+urllib.urlencode(data)
    else:
        data = ''
    conn.request(method, '/api/19/'+url+data, '', headers)
    response = conn.getresponse()
    return json.loads(response.read())

if __name__ == "__main__":
    main()