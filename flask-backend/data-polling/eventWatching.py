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


# DB setup 
mClient = MongoClient("mongodb://127.0.0.1:27017")
db = mClient.clusterData
eventCollection = db.clusterEventCollection
#fullEventCollection = db.clusterFullEventCollection
#fullEventCollection.drop()
eventCollection.drop()

# assumes two events cant happen at the exact same time

# K8s API setup 
# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()

# this will run indefinitely I believe
print("STARTING WATCH")
w = watch.Watch()
for w_event in w.stream(api.list_event_for_all_namespaces):
    event = {}
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
    # only add event if not already in the db (should probably check every field is the same but meh)
    eventCollection.update_one(
            { 'time': event["time"], 'message':event['message'], 'object': event['object']}, # filter
            { '$setOnInsert': event},
            upsert=True
        )
    #eventCollection.insert_one(event)
    print("Inserted ", event['message'])


print("Ended.")