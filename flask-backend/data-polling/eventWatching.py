import flask
from flask import jsonify
import json

import sys
sys.path.append("c:\python38\lib\site-packages")
#from bson import ObjectID
from bson.json_util import dumps

import kubernetes
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
from graph_pop import update_graph_data
import pickle
from pprint import pprint

'''
#### DB setup #### 
mClient = MongoClient("mongodb://127.0.0.1:27017")
db = mClient.clusterData
eventCollection = db.clusterEventCollection
topologyCollection = db.clusterTopologyCollection
#fullEventCollection = db.clusterFullEventCollection
#fullEventCollection.drop()
eventCollection.drop()
topologyCollection.drop()'''

# assumes two events cant happen at the exact same time

#### Get API Objects ####
# K8s API setup 
# configure k8s client 
configuration = config.load_kube_config()
api = client.CoreV1Api() # I don't have to call this again every time, right? 
# Apps API
api_client = kubernetes.client.ApiClient(configuration)
api2 = client.AppsV1Api(api_client)


#input("continue...")


# this will run indefinitely I believe
# before watching, figure out topology variables
# load Topology from DB, get max ids for vert_id, edge_id

# get old graph data from  
events = []
graph_data = {'vertices':[],'edges':[]}
vert_id = 0
edge_id = 0

print("STARTING WATCH")
w = watch.Watch()
for w_event in w.stream(api.list_event_for_all_namespaces):

    # update graph data each time an event is detected --> (change to only happen on certain events?)
    print("Updating graph data!")
    vert_id, edge_id = update_graph_data(api, api2, vert_id, edge_id, graph_data, 'tritium')
    #print(graph_data['vertices'])
        #, graph_data = update_graph_data(api, api2, vert_id, edge_id, graph_data)

    # write graph data to 
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
    '''eventCollection.update_one(
            { 'time': event["time"], 'message':event['message'], 'object': event['object']}, # filter
            { '$setOnInsert': event},
            upsert=True
        )'''
    #eventCollection.insert_one(event)
    ##### UPDATE GRAPH DATABASE #####
    #if len(events)%1 == 0: # every few minutes...
    #    print("SAVING TO PICKLE FILE")
        # save data to file
    events.append(event)
    with open("events.p", "wb") as f:
        pickle.dump(events, f)
    with open("graph.p", "wb") as f:
        pickle.dump(graph_data, f)

    print("Inserted ", event['message'])

print("Ended.")