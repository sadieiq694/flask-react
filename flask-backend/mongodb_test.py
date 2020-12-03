import sys
import json

sys.path.append("c:\python38\lib\site-packages")

from bson.json_util import dumps
import pymongo
from pymongo import MongoClient

def parse_json(data):
    return json.loads(dumps(data))

client = MongoClient()

db = client.myNewDatabase

collection = db.graphData

graphData = collection.find_one()

parsed_data = parse_json(graphData)

#print(parse_json(graphData))

print(graphData['nodes'][0])
print(graphData)
print(parsed_data['nodes'][0])
print(parsed_data)