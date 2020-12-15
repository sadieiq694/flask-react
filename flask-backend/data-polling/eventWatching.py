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
from datetime import datetime


import pymongo
from pymongo import MongoClient

print("STARTING")

# DB setup 
mClient = MongoClient("mongodb://127.0.0.1:27017")
db = mClient.clusterData
#graphCollection = db.graphData
eventCollection = db.clusterEventCollection
fullEventCollection = db.clusterFullEventCollection
#fullEventCollection.drop()
#eventCollection.drop()

# assumes two events cant happen at the exact same time

# K8s API setup 
# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()

# this will run indefinitely I believe
print("START!")
count = 100
w = watch.Watch()
for w_event in w.stream(api.list_event_for_all_namespaces):
    event = {}
    count -= 1
    # add the mongoDB
    item = w_event['object']
    #print(item)
    #fullEventCollection.insert_one(item)
    #print("Event: %s %s" % (item.type, item.metadata.name))
    event["type"] = item.type
    event["reason"] = item.reason
    event["message"] = item.message
    event["object"] = item.involved_object.name
    event["object-type"] = item.involved_object.kind
                
    event["time"] = item.event_time if item.event_time else item.last_timestamp if item.last_timestamp else item.first_timestamp
    event["time"] = datetime.timestamp(event["time"])
    event["time"] =  str(math.trunc( event["time"]*1000))
    # only add event if not already in the db
    eventCollection.update_one(
            { 'time': event["time"]}, # filter
            { '$setOnInsert': event},
            upsert=True
        )
    #eventCollection.insert_one(event)
    print("Inserted ", event['message'])
    if not count:
        w.stop()

print("Ended.")