import flask
from flask import jsonify
import json

import sys
sys.path.append("c:\python38\lib\site-packages")
#from bson import ObjectID
from bson.json_util import dumps

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

client = MongoClient()
db = client.myNewDatabase

#graphCollection = db.graphData
#cpuCollection = db.cpuData
#errCollection = db.errData
eventCollection = db.eventData
#latencyCollection = db.latencyData
#memoryCollection = db.memoryData
#opsCollection = db.opsData

#graphData = graphCollection.find_one()
#if '_id' in graphData:
#    print("removing id")
#    del graphData['_id']
#parsedGraphData = parse_json(graphData)
#newGraphData = {}
#newGraphData['nodes'] = parsedGraphData['nodes']
#newGraphData['edges'] = parsedGraphData['edges']

#cpuData = get_dictionary_list(cpuCollection)
#errData = get_dictionary_list(errCollection)
eventData = get_dictionary_list(eventCollection)
#latencyData = get_dictionary_list(latencyCollection)
#memoryData = get_dictionary_list(memoryCollection)
#opsData = get_dictionary_list(opsCollection)
for e in eventData:
    print(e['message'])
    e['message'] = e['message'].replace('"', '') 
    print(e['message'])

#all_data = {}
#all_data['graph'] = graphData
#all_data['cpu'] = cpuData
#all_data['error'] = errData
#all_data['event'] = eventData
#all_data['latency'] = latencyData
#all_data['memory'] = memoryData
#all_data['ops'] = opsData

#print(all_data.keys())
#print(all_data['cpu'][0])
#print(all_data['error'][0])
print(all_data['event'][0])
print("added all data to dictionary")

#print(type(newGraphData))
#graph_str = json.dumps(newGraphData) # change to a string