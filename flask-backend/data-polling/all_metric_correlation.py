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

base_url = "http://prometheus.169.48.174.6.nip.io/api/v1/"

# first, get list of all metrics
metric_list_url = 'label/__name__/values'

r = requests.get(url = base_url+metric_list_url)

name_data = r.json()
name_results = name_data['data']

#print(name_results)

starttime = time.time()
end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
start_ts = end_ts - 60
very_first_start = copy(start_ts)

url_now = "&start={0}&end={1}".format(start_ts,end_ts)

# now fetch metrics for each of these!
for m in name_results: 
    cur_url = base_url + '/query_range?query=' + m + '&step=14' + url_now
    cur_r = requests.get(url= cur_url)
    cur_data = cur_r.json()
    results_stat = name_data['status']
    if results_stat != "success":
        print(m, results_stat)

print("DONE")