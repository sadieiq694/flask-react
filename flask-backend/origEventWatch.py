import sys
sys.path.append("c:\python38\lib\site-packages")
import flask
from flask import jsonify
from flaskthreads import AppContextThread
from kubernetes import client, config, watch
import json
from tabulate import tabulate
from copy import copy
from multiprocessing import Process, Manager
import time
from datetime import datetime


class processClass:
    def __init__(self):
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def run(self):
         # Run background process to watch/subscribe to kubernetes events
         subscribe()


# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api()

# setup flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# dummy endpoint
@app.route('/', methods=['GET'])
def home():
    return "<h1>Tritium Rest API</h1><p>Trial</p>"

# get all events
@app.route('/events', methods=['GET'])
def getEvents():
    # working -- get events from namespace
    events = api.list_namespaced_event(namespace = "default")
    # print(events.items[0])
    event =  { "type":"mert","reason": "Scheduled", "message":"Successfully assigned default/kubernetes-bootcamp-86656bc875-f6qkl to minikube", "object": "kubernetes-bootcamp-86656bc875-f6qkl","object-type":"Pod","time":10, "importance": 1}
    all_events = []
    print(events)
    i = 0
    for item in events.items:
        event["type"] = item.type
        event["reason"] = item.reason
        event["message"] = item.message
        event["object"] = item.involved_object.name
        event["object-type"] = item.involved_object.kind
         
        event["time"] = item.event_time if item.event_time else item.last_timestamp if item.last_timestamp else item.first_timestamp
        
        # event["time"] = time.mktime(event["time"].timetuple())
        event["time"] = datetime.timestamp(event["time"])
        event["time"] =  math.trunc( event["time"]*1000)


        # event["time"] = 55 + i
        # i = i +1
        event["importance"] = 1 if item.type == "Normal" else 5
        print(event)
        all_events.append(copy(event))
    return jsonify(all_events)


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
        print(events)


#if __name__ == '__main__':
    #freeze_support()
print("orig")
# shared list for multiprocesses
manager = Manager()
events = manager.list()

# run backgrount task
# processClass()
#run flask app
app.run(threaded=True, port =5052)