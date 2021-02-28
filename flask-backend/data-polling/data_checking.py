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
import json
import os

import pymongo
from pymongo import MongoClient
import pickle

if os.path.exists("data.p"):
    with open('graph.p', 'rb') as f:
        graph_topology = pickle.load(f)

print(graph_topology['vertices'])