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

import pymongo
from pymongo import MongoClient
import pickle
from copy import copy

# turn into function
# query every five  
# call this function to get every five minutes, to mongoDB
# base_url = "http://prometheus.169.48.174.6.nip.io/api/v1"
# base_url = "http://127.0.0.1:49381/api/v1"
base_url = "http://prometheus.169.48.174.6.nip.io/api/v1/"
quantile = 0.99
service = ".*default.svc.cluster.local"

cpu_url = base_url + '/query_range?query=container_cpu_usage_seconds_total&namespace=tr&start=1614133653.088&end=1614137253.088&step=14'

######################
### METRICS QUERY ####
# latency for service: (histogram_quantile({0}, sum(irate(istio_request_duration_milliseconds_bucket{reporter="source",destination_service=~"productpage.default.svc.cluster.local"}[1m])) by (le)) / 1000) 
url = base_url + "/query_range?query=(histogram_quantile({0}%2C%20sum(irate(istio_request_duration_milliseconds_bucket%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{1}%22%7D%5B1m%5D))%20by%20(le))%20%2F%201000)%20&step=5"

# latency for each service: rate(istio_request_duration_milliseconds_sum{reporter="destination"}[1m])/rate(istio_request_duration_milliseconds_count{reporter="destination"}[1m])
# Train Ticket
url_latency = 'query_range?query=rate(istio_request_duration_milliseconds_sum%7Breporter%3D%22destination%22%2C%20namespace%3D%22tr%22%7D%5B1m%5D)%2Frate(istio_request_duration_milliseconds_count%7Breporter%3D%22destination%22%2C%20namespace%3D%22tr%22%7D%5B1m%5D)&step=5'
# bookinfo
#url_latency = base_url + "/query_range?query=rate(istio_request_duration_milliseconds_sum{reporter=%22destination%22}[1m])/rate(istio_request_duration_milliseconds_count{reporter=%22destination%22}[1m])&step=5"

# VOLUME round(sum(irate(istio_requests_total{reporter="destination"}[1m])), 0.001)


# numerator:     sum(irate(istio_requests_total{reporter="source", destination_service=~"productpage.default.svc.cluster.local",response_code!~"5.*", source_workload=~"istio-ingressgateway", source_workload_namespace=~"istio-system"}[5m])) by (source_workload, source_workload_namespace)
# denominator:   sum(irate(istio_requests_total{reporter="source", destination_service=~"productpage.default.svc.cluster.local", source_workload=~"istio-ingressgateway", source_workload_namespace=~"istio-system"}[5m])) by (source_workload, source_workload_namespace)
#url_error = base_url + "/query_range?query=sum(irate(istio_requests_total%7Breporter%3D%22source%22%2C%20destination_service%3D~%22{0}%22%2Cresponse_code!~%225.*%22%2C%20source_workload%3D~%22istio-ingressgateway%22%2C%20source_workload_namespace%3D~%22istio-system%22%7D%5B5m%5D))%20by%20(source_workload%2C%20source_workload_namespace)%20%2F%20sum(irate(istio_requests_total%7Breporter%3D%22source%22%2C%20destination_service%3D~%22{0}%22%2C%20source_workload%3D~%22istio-ingressgateway%22%2C%20source_workload_namespace%3D~%22istio-system%22%7D%5B5m%5D))%20by%20(source_workload%2C%20source_workload_namespace)&step=5"

# updated # sum(irate(istio_requests_total{reporter="source",destination_service=~"reviews.default.svc.cluster.local",response_code!~"5.*"}[5m]))
url_error = base_url + "/query_range?query=sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%2Cresponse_code!~%225.*%22%7D%5B5m%5D))%20%2F%20sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%7D%5B5m%5D))&step=5"

# cpu rate(container_cpu_usage_seconds_total{ image!="", container_name!="POD"}[5m])
# https://itnext.io/k8s-monitor-pod-cpu-and-memory-usage-with-prometheus-28eec6d84729
url_cpu = base_url + "/query_range?query=rate(container_cpu_usage_seconds_total{namespace={tr},container!=%22POD%22,image!=%22%22}[5m])&step=5" # != pod????
url_memory = base_url + "/query_range?query=container_memory_working_set_bytes{namespace={tr},container!=%22POD%22,image!=%22%22}&step=5"
###########################
###########################

# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()


def get_metrics( url_formatted, quantile_arg = 0):
    if quantile_arg != 0:
        url_formatted = url_formatted.format(quantile_arg)
    #else:
    #    url_formatted = url.format(service)
    #print(url_formatted)
    #input("Continue...")
    res = []
    r = requests.get(url = url_formatted) 
  
    # extracting data in json format 
    data = r.json()
    for item in data["data"]["result"]:
        cur_result = {}
        cur_result["metadata"] = item["metric"]
        cur_result["values"] = []
        for item2 in item["values"]:
#           print(item2)
            item2[1] = float(item2[1])
            cur_result["values"].append([item2[0], item2[1]* 1000 if (not(math.isnan(item2[1]))) else 0])
        res.append(copy(cur_result))
    return res

def fetch_lat_data(url):
    #latency = {"resource_id":service,"lat":0,"quantile":0,"time":0}
    #res_lat_50 = []
    #res_lat_90 = [] 
    #res_lat_99 = [] 
      
    res_lat_50 = get_metrics(url, 0.50)
    res_lat_90 = get_metrics(url, 0.90)
    res_lat_99 = get_metrics(url, 0.99)
    reg = get_metrics(url)

    # print(res_lat)   
    all_lat = {"50th": res_lat_50, "90th": res_lat_90, "99th": res_lat_99, "reg":reg} 
    return all_lat

def fetch_mem_data(url_now):
    r = requests.get(url = url_now) 
  
    # extracting data in json format 
    mem_data = r.json()
    mem_results = mem_data["data"]["result"]
    
    mem_formatted = []
    mem = {}

    for item in mem_results:
        try:
            #print(item['metric']['pod'], item['metric']['container'], item['metric']['namespace'])
            resource_id =  item["metric"]["pod"] + "/" +  (item["metric"]["container"] if "container" in item["metric"] else "")
            if item['metric']['container'] != 'istio-proxy': 
                for value in item["values"]:
                    time = math.trunc(value[0]*1000)
                    idx = next((index for (index, d) in enumerate(mem_formatted) if d["time"] == time), None)
                    if idx is None: #not any(d.get('time') == time for d in cpu_formatted): # cpu['time'] in cpu_formatted:
                        # need to append a new guy!
                        mem["time"] = time
                        mem[resource_id] = float(value[1])
                        mem_formatted.append(copy(mem))
                    else:
                        # this time already exists in the dictionary, get index of the time, to work with recharts, 
                        mem_formatted[idx][resource_id] = float(value[1])
        except:
            continue
    return mem_formatted

def fetch_cpu_data(url_now): 
    cpu_formatted = []
    r_cpu = requests.get(url = url_now) 

    cpu_data = r_cpu.json()
    cpu_results = cpu_data['data']['result']

    cpu = {}

    for item in cpu_results: # one item per object I think...
        try:
            resource_id =  item["metric"]["pod"] + "/" +  (item["metric"]["container"] if "container" in item["metric"] else "")
            if item['metric']['container'] != 'istio-proxy': 
                for value in item["values"]:
                    time = math.trunc(value[0]*1000)
                    idx = next((index for (index, d) in enumerate(cpu_formatted) if d["time"] == time), None)
                    if idx is None: #not any(d.get('time') == time for d in cpu_formatted): # cpu['time'] in cpu_formatted:
                        # need to append a new guy!
                        cpu["time"] = time
                        cpu[resource_id] = float(value[1])
                        cpu_formatted.append(copy(cpu))
                    else:
                        # this time already exists in the dictionary, get index of the time,  
                        # to work with recharts, 
                        cpu_formatted[idx][resource_id] = float(value[1])
        except:
            continue
    # WRITE TO MONGODB
    return cpu_formatted

def fetch_volume_data(url_now): 
    volume_array = [] 
    r_volume = requests.get(url = url_now) 

    volume_data = r_volume.json()
    volume_results = volume_data['data']['result'][0]

    for val in volume_results['values']:
        volume_array.append([val[0], float(val[1])])

    return volume_array


# Configurable time interval 
# Kiali for service-service relationships 
# end to end traces? 
# Something like this?
import time
#very_start = time.time()
print("START")

'''if os.path.exists("data.p"):
    with open('data.p', 'rb') as f:
        all_data = pickle.load(f)
else:'''
all_data = {"cpu_data":[], "memory_data":[], "latency_data": [], "ops_data":[], "error_data":[], "volume_data":[]}

starttime = time.time()
end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
start_ts = end_ts - 60
very_first_start = copy(start_ts)

while end_ts - very_first_start < 1200: # 15 minutes
    print(end_ts - very_first_start)
    print("tick")

    url_now = "&start={0}&end={1}".format(start_ts,end_ts)

    #url_latency = ""
    cpu_url_namespaced = base_url + "query_range?query=container_cpu_usage_seconds_total%7Bnamespace%3D%22tr%22%7D&step=15" #start=" + str(start_ts) + "&end=" + str(end_ts) + "&step=10" #_=1614134310140"
    memory_url_namespaced = base_url + "query_range?query=container_memory_working_set_bytes%7Bnamespace%3D%22tr%22%7D&step=15" #start=" + str(start_ts) + "&end=" + str(end_ts) + "&step=10"
    #latency_url = base_url + "query_range?query=rate(istio_request_duration_milliseconds_sum%7Breporter%3D%22destination%22%2C%20destination_service%3D~%22productpage.*%22%7D%5B1m%5D)%2Frate(istio_request_duration_milliseconds_count%7Breporter%3D%22destination%22%2C%20destination_service%3D~%22productpage.*%22%7D%5B1m%5D)&step=15" 
    latency_url = base_url + "query_range?query=rate(istio_request_duration_milliseconds_sum%7Breporter%3D%22destination%22%2C%20namespace%3D%22tr%22%7D%5B1m%5D)%2Frate(istio_request_duration_milliseconds_count%7Breporter%3D%22destination%22%2C%20namespace%3D%22tr%22%7D%5B1m%5D)&step=15"
    #error_url_namespaced = 
    # error_url = base_url + "query_range?query=sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%2Cresponse_code!~%225.*%22%7D%5B5m%5D))%20%2F%20sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%7D%5B5m%5D))&step=5"
    # CHANGE!!!
    volume_productpage = base_url + "query_range?query=round(sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22productpage.tritium.svc.cluster.local%22%7D%5B5m%5D))%2C%200.001)&step=15"
    volume_travelservice = base_url + 'round(sum(irate(istio_requests_total%7Breporter%3D"destination"%2C%20destination_service%3D"ts-travel-service.tr.svc.cluster.local"%2C%20namespace%3D"tr"%7D%5B1m%5D))%2C%200.001)&step=15'
    ### RUN EVERY FETCH FUNCTION

    ### LATENCY ### # NOT TESTED!

    ### CPU ###
    cpu_new_data = fetch_cpu_data(cpu_url_namespaced + url_now)
    #times = [i['time'] for i in cpu_new_data]
    #print(times)
    all_data['cpu_data'].extend(cpu_new_data[1:])
    
    ### MEMORY ###
    mem_new_data = fetch_mem_data(memory_url_namespaced + url_now)
    all_data['memory_data'].extend(mem_new_data[1:])

    ### VOLUME ### 
    volume_new_data = fetch_volume_data(volume_travelservice + url_now)
    all_data['volume_data'].extend(volume_new_data)

    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
    start_ts = end_ts - 60

print("EXITED LOOP")

url_all = "&start={0}&end={1}".format(very_first_start, end_ts)
latency_data = fetch_lat_data(latency_url + url_all)
#print(latency_new_data)
print(type(latency_data))
#input("Continue")
#values = [i[0]['values'] for i in latency_new_data['50th']]
#print(values)
#print(latency_new_data[0].keys())
all_data['latency_data'] = latency_data#.append(latency_new_data)

'''print(len(all_data['cpu_data']))
    if len(all_data['cpu_data'])%20 == 0: # every few minutes...
        print("SAVING TO PICKLE FILE")
        # save data to file'''

with open("data.p", "wb") as f:
    pickle.dump(all_data, f)

#print ("Start")

#fetch_cpu_data(url_now)


#return jsonify(res_cpu)

'''

details_results = [i['details-v1-5974b67c8-j4bcr/details'] for i in data]
ratings_results = [i['ratings-v1-c6cdf8d98-9xkzn/ratings'] for i in data]
reviews1_results = [i['reviews-v1-7f6558b974-xwcck/reviews'] for i in data]
reviews2_results = [i['reviews-v3-cc56b578-p4824/reviews'] for i in data]
reviews3_results = [i['reviews-v2-6cb6ccd848-tzbq9/reviews'] for i in data]


print(details_results)
print(ratings_results)
print(reviews3_results)
print(reviews2_results)
print(reviews3_results)

# dummy endpoint
@app.route('/', methods=['GET'])
def home():
    return "<h1>Tritium Rest API</h1><p>Trial</p>"


# latency endpoint
@app.route('/latency', methods=['GET'])



# err endpoint
@app.route('/err', methods=['GET'])
def getErr():
    if request.args.get('start') and request.args.get('end'):
        start_ts = request.args.get('start')
        end_ts = request.args.get('end')
    else:
        end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
        start_ts = end_ts - 60
    success = {"resource_id":service,"success":0,"time":0}
    url_now = "&start={0}&end={1}".format(start_ts,end_ts) 
    res_suc = []
    err = get_metrics(url_error+url_now)
#     print(err)

    for item in err:
        success["time"] =  math.trunc(item[0]*1000)
        success["success"] = item[1] if (not(math.isnan(item[1])))  else 1
        res_suc.append(copy(success))
    return jsonify(res_suc)


# ops endpoint
@app.route('/ops', methods=['GET'])
def getOps():
    if request.args.get('start') and request.args.get('end'):
        start_ts = request.args.get('start')
        end_ts = request.args.get('end')
    else:
        end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
        start_ts = end_ts - 60

    vol = {"resource_id":service,"ops":0,"time":0}
    res_vol = []
    url_now = "&start={0}&end={1}".format(start_ts,end_ts)
    
    volume = get_metrics(url_volume+url_now)
    
    for item in volume:
        vol["time"] =  math.trunc(item[0]*1000)
        vol["ops"] = item[1] if (not(math.isnan(item[1])))  else 0
        res_vol.append(copy(vol))
    return jsonify(res_vol)

#run flask app
app.run(threaded=True, port =5051 )'''
