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
import os
import numpy as np 
import pickle
from copy import copy

print("START")

base_url = "http://prometheus.169.48.174.6.nip.io/api/v1/"

# first, get list of all metrics
metric_list_url = 'label/__name__/values'

r = requests.get(url = base_url+metric_list_url)

name_data = r.json()
name_results = name_data['data']

#print(name_results)

end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
start_ts = end_ts - 1260
very_first_start = copy(start_ts)

url_now = "&start={0}&end={1}".format(start_ts,end_ts)

all_data = [] # list to hold all data

# now fetch metrics for each of these!
for m in name_results: 
    cur_url = base_url + 'query_range?query=' + m + '%7Bnamespace%3D%22tritium%22%7D&step=5' + url_now
    cur_r = requests.get(url= cur_url)
    cur_data = cur_r.json()
    results_stat = name_data['status']
    if results_stat != "success":
        print(m, results_stat)
    else:
        all_data.append({m:cur_data['data']})


cpu_url_namespaced = base_url + "query_range?query=container_cpu_usage_seconds_total%7Bnamespace%3D%22tritium%22%7D&step=5" #start=" + str(start_ts) + "&end=" + str(end_ts) + "&step=10" #_=1614134310140"
memory_url_namespaced = base_url + "query_range?query=container_memory_working_set_bytes%7Bnamespace%3D%22tritium%22%7D&step=5" #start=" + str(start_ts) + "&end=" + str(end_ts) + "&step=10"
#latency_url = base_url + "query_range?query=rate(istio_request_duration_milliseconds_sum%7Breporter%3D%22destination%22%2C%20namespace%3D%22tritium%22%7D%5B1m%5D)%2Frate(istio_request_duration_milliseconds_count%7Breporter%3D%22destination%22%2C%20namespace%3D%22tritium%22%7D%5B1m%5D)&step=5"
latency_url = base_url + 'query_range?query=rate(istio_request_duration_milliseconds_sum%7Breporter%3D"destination"%2Cnamespace%3D"tritium"%7D%5B1m%5D)%2Frate(istio_request_duration_milliseconds_count%7Breporter%3D"destination"%2C%20namespace%3D"tritium"%7D%5B1m%5D)&step=5'
volume_productpage = base_url + "query_range?query=round(sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22productpage.tritium.svc.cluster.local%22%7D%5B5m%5D))%2C%200.001)&step=5"
error_url = base_url + 'query_range?query=sum(irate(istio_requests_total%7Breporter%3D"source"%2Cnamespace%3D"tritium"%2Cresponse_code!~"5.*"%7D%5B5m%5D))&step=5'
custom_queries = [cpu_url_namespaced, memory_url_namespaced, latency_url, volume_productpage, error_url]

for cq in custom_queries:
    cur_url = cq + url_now 
    cur_r = requests.get(url= cur_url)
    cur_data = cur_r.json()
    results_stat = name_data['status']
    if results_stat != "success":
        print(cq, results_stat)
    else:
        all_data.append({cq:cur_data['data']})


with open("healthy_rollout_varying_load.p", "wb") as f:
    pickle.dump(all_data, f)

print("DONE")