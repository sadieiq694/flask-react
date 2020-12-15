import flask
from flask import jsonify, request
import json

import sys
sys.path.append("c:\python38\lib\site-packages")
#from bson import ObjectID
from bson.json_util import dumps

from kubernetes import client, config, watch
from tabulate import tabulate
from copy import copy
from multiprocessing import Process, Manager
import time
from datetime import datetime
import math

import pymongo
from pymongo import MongoClient

def parse_json(data):
    return json.loads(dumps(data))

def get_dictionary_list(coll):
    # convert all dictionaries to proper data formats, remove 'id' key
    dict_list = []
    for elem in coll.find():
        parsed_elem = parse_json(elem)
        if '_id' in parsed_elem:
            del parsed_elem['_id']
        dict_list.append(parsed_elem)
    return dict_list

'''class processClass:
    def __init__(self):
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def run(self):
         # Run background process to watch/subscribe to kubernetes events
         subscribe()'''

# DB setup 
mClient = MongoClient()
db = mClient.myNewDatabase

db_e = mClient.clusterData
#graphCollection = db.graphData
eventCollection = db_e.clusterEventCollection

graphCollection = db.graphData
cpuCollection = db.cpuData
errCollection = db.errData
#eventCollection = db.eventData
latencyCollection = db.latencyData
memoryCollection = db.memoryData
opsCollection = db.opsData

db2 = mClient.clusterData
eventColl = db2.clusterEventCollection

# K8s API setup 
# configure k8s client 
#config.load_kube_config()
#api = client.CoreV1Api()

# setup flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True
# app = flask.Flask(__name__)


@app.route('/data/graph', methods=['GET'])
def graph_data():
    graphData = graphCollection.find_one()
    if '_id' in graphData:
        print("removing id")
        del graphData['_id']
    parsedGraphData = parse_json(graphData)
    return jsonify(parsedGraphData)

@app.route('/data/metric', methods=['GET'])
def metric_data():
    print("Fetching from metric_data endpoint")
    cpuData = get_dictionary_list(cpuCollection)
    for c in cpuData:
        c['cpu'] = float(c['cpu'])
    errData = get_dictionary_list(errCollection)
    eventData = get_dictionary_list(eventCollection)
    for e in eventData:
        #print(e['message'])
        e['message'] = e['message'].replace('"', '') 
        #print(e['message'])
    latencyData = get_dictionary_list(latencyCollection)
    memoryData = get_dictionary_list(memoryCollection)
    for m in memoryData:
        m['memory'] = int(m['memory'])
    opsData = get_dictionary_list(opsCollection)
    metric_data = {}
    #all_data['graph'] = parsedGraphData
    metric_data['cpu'] = cpuData
    metric_data['error'] = errData
    metric_data['event'] = eventData
    metric_data['latency'] = latencyData
    metric_data['memory'] = memoryData
    metric_data['ops'] = opsData   
    return jsonify(metric_data) 


@app.route("/")
def my_index():
    return flask.render_template("index.html")

'''# background task to watch events
def subscribe():
    print("BG-MERT")
    # watch events
    event =  { "type":"mert","reason": "Scheduled", "message":"Successfully assigned default/kubernetes-bootcamp-86656bc875-f6qkl to minikube", "object": "kubernetes-bootcamp-86656bc875-f6qkl","object-type":"Pod","time":10, "importance": 1}
    # events = 
    count = 100
    w = watch.Watch()
    for w_event in w.stream(api.list_namespaced_event, namespace="default", _request_timeout=60):
        # print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        # print(item)
        item = w_event['object']
        event["type"] = item.type
        event["reason"] = item.reason
        event["message"] = item.message
        event["object"] = item.involved_object.name
        event["object-type"] = item.involved_object.kind
        event["time"] = item.event_time if item.event_time else item.last_timestamp if item.last_timestamp else item.first_timestamp
        event["time"] =  math.trunc( event["time"]*1000)
        events.append(copy(event))
        # Add to mongo db
        
        print(events)'''

if __name__ == "__main__":
    # shared list for multiprocesses
    #manager = Manager()
    #events = manager.list()

    # run backgrount task
    # processClass()
    #run flask app
    #print("running")
    #app.run(threaded=True, port =5052)
    app.run(debug=True, port=2000)