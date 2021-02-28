import time
from datetime import datetime, timedelta
import math 

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

#######################
###### FUNCTIONS ######
####################### (put these in a separate file! This is messy)

# takes a vertex index, returns indices of all edges connected to it
def connectedEdges(graph_data, idx):
    connected_edges = [dic for dic in graph_data['edges'] if (dic['source'] == idx or dic['target'] == idx)]
    return connected_edges

def time_formatting(time_value):
    return math.trunc(datetime.timestamp(time_value)*1000)
    #return formatted_time

def termination_times(dics_to_delete, graph_data):
    for dic in dics_to_delete:
        dic['termination_time'] = time_formatting(datetime.now())
        # also need to delete all edges to this node
        d_edges = connectedEdges(graph_data, dic['id'])
        for edge_dic in d_edges:
            edge_dic['termination_time'] = time_formatting(datetime.now())

def add_container(c, graph_data, vert_id, edge_id, pod):
    new_cont = {}
    new_cont['id'] = vert_id
    new_cont['name'] = c.name
    new_cont['group'] = 'container'
    new_cont['pod'] = pod.metadata.name
    new_cont['image'] = c.image
    new_cont['resources'] = c.resources
    if new_cont['resources'].limits is None:
        new_cont['resources'].limits = ""
    if new_cont['resources'].requests is None:
        new_cont['resources'].requests = ""
    new_cont['activation_time'] = time_formatting(pod.metadata.creation_timestamp)
    term_time = datetime.now() + timedelta(weeks=500)
    new_cont['termination_time'] = time_formatting(term_time)
    # create edge
    cont_edge = {}
    cont_edge['id'] = edge_id
    cont_edge['type'] = 'runs' # pod --> container
    # get id of pod with name i.metadata.name
    source_id = [x['id'] for x in graph_data['vertices'] if x['group'] == 'pod' and x['name'] == pod.metadata.name]
    cont_edge['source'] = source_id[0]
    cont_edge['target'] = new_cont['id']
    cont_edge['activation_time'] = time_formatting(pod.metadata.creation_timestamp)
    term_time = datetime.now() + timedelta(weeks=500)
    cont_edge['termination_time'] = time_formatting(term_time)
    graph_data['edges'].append(cont_edge)
    edge_id += 1
    graph_data['vertices'].append(new_cont)
    vert_id += 1
    return vert_id, edge_id

## FUNCTIONS ###
# populate nodes
# input: vert id number, "nodes" object
# output: list of node objects, new vert id
def get_nodes(vert_id, graph_data, nodes):
    node_names = [dic['name'] for dic in graph_data['vertices'] if dic['group']=='node']
    cur_node_names = [] # all nodes detected at this time point
    for node in nodes.items:
        cur_node_names.append(node.metadata.name) # add names to list even if they are not new
        if node.metadata.name not in node_names:   # ADD NEW NODES
            cur_vert = {}
            cur_vert['name'] = node.metadata.name
            cur_vert['id'] = vert_id
            node_names.append(cur_vert['name'])
            cur_vert['group'] = "node"
            cur_addresses = node.status.addresses
            for a in cur_addresses: # can also get Hostname this way
                if a.type == 'InternalIP':
                    cur_vert['internal_ip'] = a.address
                    break
            cur_vert['cpu_capacity'] = node.status.capacity['cpu']
            cur_vert['ephemeral_storage_capacity'] = node.status.capacity['ephemeral-storage'] 
            cur_vert['mem_capacity'] = node.status.capacity['memory']
            cur_vert['pod_capacity'] = node.status.capacity['pods']
            cur_vert['activation_time'] = time_formatting(node.metadata.creation_timestamp)
            term_time = datetime.now() + timedelta(weeks=500)
            cur_vert['termination_time'] = time_formatting(term_time)
            # add allocatable here? (mem, storage, pods)
            # node.status.node_info may also be useful, this is probably fine for now    
            #print(node.metadata.name)
            graph_data['vertices'].append(cur_vert)
            vert_id += 1
    # MARK TERMINATION OF KILLED NODES
    deleted_names = [name for name in node_names if name not in cur_node_names]
    dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='node' and x['name'] in deleted_names] 
    termination_times(dics_to_delete, graph_data)
    return vert_id

# populate pods
# input: vert_id number, edge id,  "pods" object 
#       (maybe should pass in graph_data)
# output: list of pod objects, list of edges, new ids
# populate pods and containers
# input: vert_id number, edge id,  "pods" object 
#       (maybe should pass in graph_data)
# output: list of pod objects, list of edges, new ids
def get_pods_containers(vert_id, edge_id, graph_data, pods):
    pod_names = [dic['name'] for dic in graph_data['vertices'] if dic['group']=='pod']
    
    # get names for containers in each pod
    #graph_data_pods = [x for x in graph_data['vertices'] if x['group'] == 'pod']
    container_name_groups = [] # from OLD record
    for pod_name in pod_names:
        corr_container_names = [x['name'] for x in graph_data['vertices'] if x['group'] == 'container' and x['pod'] == pod_name]
        cur_dic = {}
        cur_dic['podname'] = pod_name
        cur_dic['containers'] = corr_container_names
        container_name_groups.append(cur_dic)
    # now we have dictionaries mapping pod names to the names of their containers
    
    cur_pod_names = [] # to hold names of current pods

    for pod in pods.items:
        cur_pod_names.append(pod.metadata.name)
        cur_node = pod.spec.node_name
        cur_pod_containers = []
        ################
        ### NEW PODS ###
        ################
        if pod.metadata.name not in pod_names:
            ### CREATE POD ###
            cur_vert = {}
            cur_vert['name'] = pod.metadata.name
            cur_vert['group'] = 'pod'
            cur_vert['id'] = vert_id
            cur_vert['activation_time'] = time_formatting(pod.metadata.creation_timestamp)
            term_time = datetime.now() + timedelta(weeks=500)
            cur_vert['termination_time'] = time_formatting(term_time)    
            vert_id += 1
            graph_data['vertices'].append(cur_vert)
            ### CREATE EDGE ###
            node_sched = [x for x in graph_data['vertices'] if x['group']=='node' and x['name'] == cur_node]
            node_sched = node_sched[0]
            cur_edge = {}
            cur_edge['id'] = edge_id
            cur_edge['type'] = 'scheduled on' # pod --> node
            cur_edge['source'] = cur_vert['id']
            cur_edge['target'] = node_sched['id']
            cur_edge['activation_time'] = time_formatting(datetime.now())
            term_time = datetime.now() + timedelta(weeks=500)
            cur_edge['termination_time'] = time_formatting(term_time)
            graph_data['edges'].append(cur_edge)
            edge_id += 1
            ### ADD CONTAINERS ###
            for c in pod.spec.containers:
                vert_id, edge_id = add_container(c, graph_data, vert_id, edge_id, pod)
        ###############
        ## OLD POD! ### (may need to add new containers, may need to switch node)
        ###############
        else:
            cur_vert = [x for x in graph_data['vertices'] if x['group']=='pod' and x['name'] == pod.metadata.name]
            if isinstance(cur_vert, list):
                cur_vert = cur_vert[0] 
            ### CHECK IF NODE HAS CHANGED, CHANGE NODE IF NECESSARY ###
            if cur_node != cur_vert['node']:
                # change the edge
                edge = [x for x in graph_data['edges'] if x['source'] == cur_vert['id'] and type == 'scheduled on']
                edge['termination_time'] = time_formatting(datetime.now())
                # new edge
                cur_node_idx = [x['id'] for x in graph_data['vertices'] if x['group'] == 'node' and x['name'] == cur_node]
                new_edge = {}
                new_edge['id'] = edge_id
                new_edge['type'] = 'scheduled on' # pod --> node
                new_edge['source'] = cur_vert['id']
                new_edge['target'] = cur_node_idx
                new_edge['activation_time'] = time_formatting(pod.metadata.creation_timestamp)
                term_time = datetime.now() + timedelta(weeks=500)
                new_edge['termination_time'] = time_formatting(term_time)
                graph_data['edges'].append(new_edge)
                edge_id += 1
            ### SEE IF CONTAINER LIST MATCHES ###
            # get old containers for this pod:
            old_container_list = [x['containers'] for x in container_name_groups if x['podname'] == pod.metadata.name]
            for c in pod.spec.containers:
                cur_pod_containers.append(c.name)
                if c.name not in old_container_list: # new container!
                    vert_id, edge_id = add_container(c, graph_data, vert_id, edge_id, pod)
            # SEE IF ANY CONTAINERS HAVE BEEN DELETED!
            deleted_names = [name for name in old_container_list if name not in cur_pod_containers] 
            # make sure it is a container, attached to the correct pod, and in the 'delete' list
            dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='container' and x['pod'] == pod.metadata.name and x['name'] in deleted_names] 
            termination_times(dics_to_delete, graph_data)
        #########################################
        # update these regardless of old or new #
        #########################################
        cur_vert['namespace'] = pod.metadata.namespace
        cur_vert['ip'] = pod.status.pod_ip
        cur_vert['app_label'] = pod.metadata.labels['app']
        # Maybe use all labels? metadata.labels
        cur_vert['node'] = pod.spec.node_name
    #######################################################################
    # MARK TERMINATION TIME OF DELETED PODS AND THEIR CORRESPONDING NODES #
    #######################################################################
    deleted_names = [name for name in pod_names if name not in cur_pod_names]
    pod_dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='pod' and x['name'] in deleted_names]
    container_dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='container' and x['pod'] in deleted_names]
    dics_to_delete = pod_dics_to_delete + container_dics_to_delete
    termination_times(dics_to_delete, graph_data)
    return vert_id, edge_id


# DEAL w/ REPLICAS
# deployments 1-1 w pods if there are no replicas, match up w/ labels?
def get_deployments(vert_id, edge_id, graph_data, deployments):
    dep_names = [dic['name'] for dic in graph_data['vertices'] if dic['group']=='deployment']
    cur_dep_names = [] 
    for dep in deployments.items:
        cur_dep_names.append(dep.metadata.name)
        if dep.metadata.name not in dep_names: # NEW POD
            cur_vert = {}
            cur_vert['id'] = vert_id
            cur_vert['name'] = dep.metadata.name #['name']
            cur_vert['group'] = 'deployment'
            cur_vert['namespace'] = dep.metadata.namespace
            cur_vert['replicas'] = dep.spec.replicas
            cur_vert['labels'] = dep.metadata.labels
            cur_vert['activation_time'] = time_formatting(dep.metadata.creation_timestamp)
            term_time = datetime.now() + timedelta(weeks=500)
            cur_vert['termination_time'] =  time_formatting(term_time)
            cur_app_label = dep.metadata.labels['app']
            cur_version_label = dep.metadata.labels['version']
            # INCLUDE STATUS INFO: dep.status.???
            # create edge HERE
            pod_list = [ x for x in graph_data['vertices'] if x['group'] == 'pod' and "app_label" in x and  x['app_label'] == cur_app_label and "version_label" in x and  x['version_label'] == cur_version_label]
            for p in pod_list:
                cur_edge = {}
                cur_edge['id'] = edge_id
                cur_edge['type'] = 'owns' # deployment --> pod
                cur_edge['source'] = cur_vert['id'] # deployment's ID
                cur_edge['target'] = p['id']
                cur_edge['activation_time'] = time_formatting(dep.metadata.creation_timestamp)
                term_time = datetime.now() + timedelta(weeks=500)
                cur_edge['termination_time'] = time_formatting(term_time)
                graph_data['edges'].append(cur_edge)
                edge_id += 1
            graph_data['vertices'].append(cur_vert)
            vert_id += 1
    deleted_names = [name for name in dep_names if name not in cur_dep_names]
    dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='deployment' and x['name'] in deleted_names] 
    termination_times(dics_to_delete, graph_data)
    return vert_id, edge_id

# populate services
# populate services
def get_services(vert_id, edge_id, graph_data, services):
    service_names = [dic['name'] for dic in graph_data['vertices'] if dic['group']=='service']
    cur_service_names = [] 
    for serv in services.items:
        cur_service_names.append(serv.metadata.name)
        if serv.metadata.name not in service_names: # NEW POD
            cur_vert = {}
            cur_vert['id'] = vert_id
            cur_vert['namespace'] = serv.metadata.namespace
            cur_vert['name'] = serv.metadata.name
            cur_vert['group'] = 'service'
            cur_vert['ip'] = serv.spec.cluster_ip
            cur_vert['labels'] = serv.metadata.labels
            cur_vert['activation_time'] = time_formatting(serv.metadata.creation_timestamp)
            term_time = datetime.now() + timedelta(weeks=500)
            cur_vert['termination_time'] = time_formatting(term_time)
            if 'app' in cur_vert['labels']:
                cur_app_label = serv.metadata.labels['app']
                cur_vert["namespace"] = serv.metadata.namespace
                pod_list = [ x for x in graph_data['vertices'] if x['group'] == 'pod' and "app_label" in x and x['app_label'] == cur_app_label]
                for pod in pod_list:
                    # pods targeted by this cluster 
                    cur_edge = {}
                    cur_edge['id'] = edge_id
                    cur_edge['type'] = 'targets' # deployment --> pod
                    cur_edge['source'] = cur_vert['id'] # deployment's ID
                    cur_edge['target'] = pod['id']
                    cur_edge['activation_time'] = time_formatting(serv.metadata.creation_timestamp)
                    term_time = datetime.now() + timedelta(weeks=500)
                    cur_edge['termination_time'] = time_formatting(term_time)
                    graph_data['edges'].append(cur_edge)
                    edge_id += 1
            graph_data['vertices'].append(cur_vert)
            vert_id += 1
    deleted_names = [name for name in service_names if name not in cur_service_names]    
    dics_to_delete = [x for x in graph_data['vertices'] if x['group']=='service' and x['name'] in deleted_names] 
    termination_times(dics_to_delete, graph_data)
    return vert_id, edge_id

def update_graph_data(api, api2, vert_id, edge_id, graph_data, namespace):
    # API calls to update data

    nodes = api.list_node()
    
    pods = api.list_namespaced_pod(namespace=namespace)
    #print(len(pods.items))
    deployments = api2.list_namespaced_deployment(namespace=namespace)
#     print(deployments)
    services = api.list_namespaced_service(namespace=namespace)

    # nodes
    vert_id = get_nodes(vert_id, graph_data, nodes)
    # pods, containers
    vert_id, edge_id = get_pods_containers(vert_id, edge_id, graph_data, pods)
    # deployments
    vert_id, edge_id = get_deployments(vert_id, edge_id, graph_data, deployments)
    # services
    vert_id, edge_id = get_services(vert_id, edge_id, graph_data, services)
    
    return vert_id, edge_id #, copy(graph_data) # could just find max idxs every time... maybe would be better


#### Get API Objects ####
# K8s API setup 
# configure k8s client 
config.load_kube_config()
api = client.CoreV1Api() # I don't have to call this again every time, right? 
# Apps API
configuration = config.load_kube_config()

#api2 = kubernetes.client.AppsV1Api(client.ApiClient(configuration))
#deployments = api2.list_namespaced_deployment(namespace="tritium")
#print(deployments)
nodes = api.list_node()
print(nodes)

# this will run indefinitely I believe
# before watching, figure out topology variables
# load Topology from DB, get max ids for vert_id, edge_id

'''
# get old graph data from  
graph_data = {}
vert_id = 0
edge_id = 0

print('Updating graph!')
vert_id, edge_id = update_graph_data(api, api2, vert_id, edge_id, graph_data)
print("Number of vertices in graph", len(graph_data['vertices']))
'''