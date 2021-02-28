import sys
sys.path.append("c:\python38\lib\site-packages")

import flask
from flask import jsonify, request
from kubernetes import client, config, watch
import json
from tabulate import tabulate
from copy import copy
import requests 
from datetime import datetime,timedelta
import time
#import matplotlib.pyplot as plt
import math
import json

import pymongo
from pymongo import MongoClient

'''
jaeger_base_url = "http://tracing.169.48.174.6.nip.io/jaeger/api/"
# prometheus_base_url 

# get list of services to iterate though for trace collection

config.load_kube_config()
api = client.CoreV1Api() # I don't have to call this again every time, right? 


services = api.list_namespaced_service(namespace="tritium")

trace_service_names = []

cur_time = time.time()*10000000
print("Current time:", cur_time)
start_time = str(1612885533265000)
end_time = 1612889278431000
#          1613584333876524 

for serv in services.items:
    #print(serv.metadata.name)
    trace_service_names.append(serv.metadata.name + '.tritium')

    #http://tracing.169.48.174.6.nip.io/jaeger/api/services/productpage.tritium/operations
    #'http://tracing.169.48.174.6.nip.io/jaeger/api/traces?end=1612990637869000&limit=20&lookback=2d&maxDuration&minDuration&service=productpage.tritium&start=1612817837869000'

print(trace_service_names)

for service in trace_service_names: 
    url = 'http://tracing.169.48.174.6.nip.io/jaeger/api/traces?end=' + str(end_time) + '&service=' + service + '&start=' + str(start_time)
    #url = 'http://tracing.169.48.174.6.nip.io/jaeger/api/traces?end=1613584333876524&limit=20&lookback=2d&maxDuration&minDuration&service=productpage.tritium&start=1613584333726524'

    print(url)
    r = requests.get(url = url) 
    #print(type(r))
    data = r.json()

    for instance in data['data']:
        print(len(instance['processes'].keys()))
        if len(instance['processes'].keys() < 3): # this is just with the istio-ingressgateway
        #if instance['processes']
    #print(spans['data'])
    #print(len(spans['data']))
    #print(spans['data'][0]['spans'][0]['processes'])
    #input("Continue...")
    #mem_results = mem_data["data"]["result"]
'''

'''nodes = {"productpage", "details", "reviews", "ratings"} # these are our SERVICES
edges = {}
# edge format: edge1 = {"source":"node1", "target":"node2", "trace_id":"something"} # source will be the upstream service

with open('example_traces.json') as f:
    data = json.load(f)

for trace in data['data']:
    #print("One trace")
    cur_trace_id = trace['traceID']
    #print(cur_trace_id)
    spans = []
    for span in trace['spans']:
        cur_span = {'id':span['spanID'], 'operationName':span['operationName'], 'startTime':span['startTime'], 'duration':span['duration']}
        for r in span['references']:
            if r['refType'] == "CHILD_OF":
                cur_span['parent'] = r['spanID']
                # This is where I would create the 
        print(cur_span)'''


kiali_request_url = 'http://kiali.169.48.174.6.nip.io/kiali/api/namespaces/graph?duration=600s&graphType=versionedApp&injectServiceNodes=true&groupBy=app&appenders=deadNode,sidecarsCheck,serviceEntry,istio&namespaces=tritium' 
# Make call to this API every x seconds


with open('example_kiali.json') as f:
    data = json.load(f)

nodes = []
edges = []
for node in data['elements']['nodes']:
    if node['data']['nodeType'] == "service":
        cur_group = "service"
        cur_name = node['data']['service']
    elif node['data']['nodeType']=="app" and 'workload' in node['data']:
        cur_group = "deployment"
        cur_name = node['data']['workload']
    else: 
        continue
    cur_node = {
        'id':node['data']['id'],
        'group':cur_group,
        'name': cur_name
    }
    nodes.append(cur_node)
print(nodes)
print("NUMBER OF NODES:", len(nodes))

for edge in data['elements']['edges']:
    source_node = next((i for i, item in enumerate(nodes) if item["id"] == edge['data']['source']), None)
    target_node = next((i for i, item in enumerate(nodes) if item["id"] == edge['data']['target']), None)
    #if source_node['group']==deployment:
    #    edge_type = ''
    #elif:
    #    edge_type = ''
    cur_edge = {
        'source': edge['data']['source'],
        'target': edge['data']['target']
    #    'edge_type': edge_type
    }
    edges.append(cur_edge)

print(edges)
print("NUMBER OF edges:", len(edges))