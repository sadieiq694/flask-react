import flask
from flask import jsonify
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

class processClass:
    def __init__(self):
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def run(self):
         # Run background process to watch/subscribe to kubernetes events
         subscribe()

# DB setup 
mClient = MongoClient()
db = mClient.myNewDatabase
graphCollection = db.graphData
eventCollection = db.eventCollection

# K8s API setup 
# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()

# setup flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True
# app = flask.Flask(__name__)


# dummy endpoint
@app.route('/', methods=['GET'])
def home():
    out = "<h1>Tritium Rest API \n"
    out += "num events: "
    out += str(eventCollection.count())
    out += "</h1><p>Trial</p>"
    return out

# watch events -- to be modiified 
@app.route('/watch', methods=['GET'])
def watchEvents():
    print("*******\n")
    print(events)
    return jsonify(list(events))

# background task to watch events
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
        collection.insert(event)
        print("inserted to mongo!", event['message'])
        # Add to mongo db
        
        print(events)

if __name__ == "__main__":
    # shared list for multiprocesses
    manager = Manager()
    events = manager.list()

    # run backgrount task
    # processClass()
    #run flask app
    print("running")
    app.run(threaded=True, port =5052)
    #app.run(debug=True, port=2000)