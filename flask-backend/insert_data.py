import sys
sys.path.append("c:\python38\lib\site-packages")
import pymongo
from pymongo import MongoClient
import json

''' Script to insert_one static data into mongoDB collections '''

# have a collection in mongoDB for each data type
# already added this 
with open('./data/graph.json') as f:
    graphData = json.load(f)

with open('./data/cpu.json') as f:
    cpuData = json.load(f)

with open('./data/err.json') as f:
    errData = json.load(f)

with open('./data/events.json') as f:
    eventData = json.load(f)

with open('./data/latency.json') as f:
    latencyData = json.load(f)

with open('./data/memory.json') as f:
    memoryData = json.load(f)

with open('./data/ops.json') as f:
    opsData = json.load(f)

# data is now in a python dictionary
#print(data['nodes'][0])
# insert dictionary into database
client = MongoClient()
db = client.myNewDatabase

graphCollection = db.graphData
graphCollection.drop()

cpuCollection = db.cpuData
cpuCollection.drop()

errCollection = db.errData
errCollection.drop()

eventCollection = db.eventData
eventCollection.drop()

latencyCollection = db.latencyData
latencyCollection.drop()

memoryCollection = db.memoryData
memoryCollection.drop()

opsCollection = db.opsData
opsCollection.drop()

# insert_one for a single object, insert_many for a list
graphCollection.insert_one(graphData) # obj
cpuCollection.insert_many(cpuData)
errCollection.insert_many(errData)
eventCollection.insert_many(eventData)
latencyCollection.insert_many(latencyData)
memoryCollection.insert_many(memoryData)
opsCollection.insert_many(opsData)

print("filled database with static data")
