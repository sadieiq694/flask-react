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

import pymongo
from pymongo import MongoClient

# turn into function
# query every five  
# call this function to get every five minutes, to mongoDB
#base_url = "http://prometheus.169.48.174.6.nip.io/api/v1"
base_url = "http://127.0.0.1:52469/"
quantile = 0.99
start = 1594150127.950368
end = 1594150147.950434
service = ".*default.svc.cluster.local"

######################
### METRICS QUERY ####
# latency for service: (histogram_quantile({0}, sum(irate(istio_request_duration_milliseconds_bucket{reporter="source",destination_service=~"productpage.default.svc.cluster.local"}[1m])) by (le)) / 1000) 
url = base_url + "/query_range?query=(histogram_quantile({0}%2C%20sum(irate(istio_request_duration_milliseconds_bucket%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{1}%22%7D%5B1m%5D))%20by%20(le))%20%2F%201000)%20&step=5"

# latency for each services: rate(istio_request_duration_milliseconds_sum{reporter="destination"}[1m])/rate(istio_request_duration_milliseconds_count{reporter="destination"}[1m])
url_latency = base_url + "/query_range?query=rate(istio_request_duration_milliseconds_sum{reporter=%22destination%22}[1m])/rate(istio_request_duration_milliseconds_count{reporter=%22destination%22}[1m])&step=5"

# global request volume  round(sum(irate(istio_requests_total{reporter="destination"}[1m])), 0.001)
# productpage volume:    round(sum(irate(istio_requests_total{reporter="source",destination_service=~"productpage.default.svc.cluster.local"}[5m])), 0.001)
url_volume = base_url + "/query_range?query=round(sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%7D%5B5m%5D))%2C%200.001)&step=5"

# numerator:     sum(irate(istio_requests_total{reporter="source", destination_service=~"productpage.default.svc.cluster.local",response_code!~"5.*", source_workload=~"istio-ingressgateway", source_workload_namespace=~"istio-system"}[5m])) by (source_workload, source_workload_namespace)
# denominator:   sum(irate(istio_requests_total{reporter="source", destination_service=~"productpage.default.svc.cluster.local", source_workload=~"istio-ingressgateway", source_workload_namespace=~"istio-system"}[5m])) by (source_workload, source_workload_namespace)
#url_error = base_url + "/query_range?query=sum(irate(istio_requests_total%7Breporter%3D%22source%22%2C%20destination_service%3D~%22{0}%22%2Cresponse_code!~%225.*%22%2C%20source_workload%3D~%22istio-ingressgateway%22%2C%20source_workload_namespace%3D~%22istio-system%22%7D%5B5m%5D))%20by%20(source_workload%2C%20source_workload_namespace)%20%2F%20sum(irate(istio_requests_total%7Breporter%3D%22source%22%2C%20destination_service%3D~%22{0}%22%2C%20source_workload%3D~%22istio-ingressgateway%22%2C%20source_workload_namespace%3D~%22istio-system%22%7D%5B5m%5D))%20by%20(source_workload%2C%20source_workload_namespace)&step=5"

# updated # sum(irate(istio_requests_total{reporter="source",destination_service=~"reviews.default.svc.cluster.local",response_code!~"5.*"}[5m]))
url_error = base_url + "/query_range?query=sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%2Cresponse_code!~%225.*%22%7D%5B5m%5D))%20%2F%20sum(irate(istio_requests_total%7Breporter%3D%22source%22%2Cdestination_service%3D~%22{0}%22%7D%5B5m%5D))&step=5"

# cpu rate(container_cpu_usage_seconds_total{ image!="", container_name!="POD"}[5m])
# https://itnext.io/k8s-monitor-pod-cpu-and-memory-usage-with-prometheus-28eec6d84729
url_cpu = base_url + "/query_range?query=rate(container_cpu_usage_seconds_total{namespace=%22default%22,container!=%22POD%22,image!=%22%22}[5m])&step=5" # != pod????
url_memory = base_url + "/query_range?query=container_memory_working_set_bytes{namespace=%22default%22,container!=%22POD%22,image!=%22%22}&step=5"
###########################
###########################

# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()

# setup flask application
#app = flask.Flask(__name__)


#if request.args.get('start') and request.args.get('end'):
#    start_ts = request.args.get('start')
#    end_ts = request.args.get('end')
#else:
end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
start_ts = end_ts - 60

url_now = "&start={0}&end={1}".format(start_ts,end_ts)
print(url_cpu +url_now)

print("MAKING REQUEST")
r = requests.get(url = url_cpu +url_now) 

print("REQUEST: ", r)

# extracting data in json format 
data = r.json()
res_cpu = []
cpu = {"resource_id": "minikube", "cpu": 323, "time": 1}

for item in data["data"]['result']:
    print(item)
    cpu["resource_id"] = item["metric"]["pod"] + "/" +  (item["metric"]["container"] if "container" in item["metric"] else "")
    for value in item["values"]:
        cpu["cpu"] = value[1]
        cpu["time"] = math.trunc(value[0]*1000)
        res_cpu.append(copy(cpu))
#return jsonify(res_cpu)

'''
# mem endpoint
@app.route('/memory', methods=['GET'])
def getMem():
    if request.args.get('start') and request.args.get('end'):
        start_ts = request.args.get('start')
        end_ts = request.args.get('end')
    else:
        end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
        start_ts = end_ts - 60
    
    url_now = "&start={0}&end={1}".format(start_ts,end_ts)
    print(url_memory +url_now)
    r = requests.get(url = url_memory +url_now) 
  
    # extracting data in json format 
    data = r.json()
    res_mem = []
    mem = {"resource_id": "minikube", "memory": 323, "time": 1}

    for item in data["data"]['result']:
        # print(item)
        mem["resource_id"] = item["metric"]["pod"] + "/" +  (item["metric"]["container"] if "container" in item["metric"] else "")
        for value in item["values"]:
            mem["memory"] = value[1]
            mem["time"] = math.trunc(value[0]*1000)
            res_mem.append(copy(mem))
    return jsonify(res_mem)


def get_metrics( url, quantile_arg = 0):
    if quantile_arg != 0:
        url_formatted = url.format(quantile_arg,service)
    else:
        url_formatted = url.format(service)
    print(url_formatted)
    res = []
    r = requests.get(url = url_formatted) 
  
    # extracting data in json format 
    data = r.json()
#     print(data)
    for item in data["data"]["result"]:
        for item2 in item["values"]:
#             print(item2)
            item2[1] = float(item2[1])
            res.append(item2)
    return res

# dummy endpoint
@app.route('/', methods=['GET'])
def home():
    return "<h1>Tritium Rest API</h1><p>Trial</p>"


# latency endpoint
@app.route('/latency', methods=['GET'])
def getLatency():
    if request.args.get('start') and request.args.get('end'):
        start_ts = request.args.get('start')
        end_ts = request.args.get('end')
    else:
        end_ts = datetime.timestamp(datetime.now().replace(microsecond=0))
        start_ts = end_ts - 60

    latency = {"resource_id":service,"lat":0,"quantile":0,"time":0}
    res_lat = []
    
    url_now = "&start={0}&end={1}".format(start_ts,end_ts)
  
    res_50 = get_metrics(url+url_now, 0.50)
    res_90 = get_metrics(url+url_now, 0.90)
    res_99 = get_metrics(url+url_now, 0.99)
    print("m")

    for item in res_50:
        latency["time"] = math.trunc(item[0]*1000)
        latency["lat"] = item[1]* 1000 if (not(math.isnan(item[1])))  else 0
        latency["quantile"] = 50
        res_lat.append(copy(latency))
        
    for item in res_90:
        latency["time"] =  math.trunc(item[0]*1000)
        latency["lat"] = item[1]* 1000 if (not(math.isnan(item[1]))) else 0
        latency["quantile"] = 90
        res_lat.append(copy(latency))
        
    for item in res_99:
        latency["time"] =  math.trunc(item[0]*1000)
        latency["lat"] = item[1]* 1000 if (not(math.isnan(item[1])))  else 0
        latency["quantile"] = 99
        res_lat.append(copy(latency))

    # print(res_lat)    
    return jsonify(res_lat)



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
