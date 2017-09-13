#!/usr/bin/env python

import parser
import os
import ruamel.yaml as YAML
import docker
import time
import requests

yaml = YAML
yaml.default_flow_style = False

# Read input files
temp_auth_data_file = os.getenv('TEMP_AUTH_DATA_FILE', '/var/lib/micado/occopus/templates/temp_auth_data.yaml')
with open(temp_auth_data_file, 'r') as f:
    temp_auth_data = yaml.round_trip_load(f, preserve_quotes=True)

temp_node_def_file = os.getenv('TEMP_NODE_DEF_FILE', '/var/lib/micado/occopus/templates/temp_node_definitions.yaml')
with open(temp_node_def_file, 'r') as f:
    temp_node_def = yaml.round_trip_load(f, preserve_quotes=True)

temp_infra_def_file = os.getenv('TEMP_INFRA_DEF_FILE', '/var/lib/micado/occopus/templates/temp_infrastructure_descriptor.yaml')
with open(temp_infra_def_file, 'r') as f:
    temp_infra_def = yaml.round_trip_load(f, preserve_quotes=True)

user_data_file = os.getenv('USER_DATA_FILE', '/var/lib/micado/occopus/templates/user_data.yaml')
with open(user_data_file, 'r') as f:
    user_data = yaml.round_trip_load(f, preserve_quotes=True)

parser.generate_auth_data(user_data, temp_auth_data)
parser.generate_node_def(user_data, temp_node_def)
parser.generate_infra_def(user_data, temp_infra_def)

auth_data_file = os.getenv('AUTH_DATA_FILE', '/etc/micado/occopus/auth_data.yaml')
if not os.path.exists(os.path.dirname(auth_data_file)):
        os.makedirs(os.path.dirname(auth_data_file))
with open(auth_data_file, 'w') as ofile:
    yaml.round_trip_dump(temp_auth_data, ofile)

node_def_file = os.getenv('NODE_DEF_FILE', '/etc/micado/occopus/nodes/node_definitions.yaml')
if not os.path.exists(os.path.dirname(node_def_file)):
        os.makedirs(os.path.dirname(node_def_file))
with open(node_def_file, 'w') as ofile:
   yaml.round_trip_dump(temp_node_def, ofile)

infra_def_file = os.getenv('INFRA_DEF_FILE', '/etc/micado/occopus/infrastructure_descriptor.yaml')
if not os.path.exists(os.path.dirname(infra_def_file)):
        os.makedirs(os.path.dirname(infra_def_file))
with open(infra_def_file, 'w') as ofile:
   yaml.round_trip_dump(temp_infra_def, ofile)

worker_infra_name = os.getenv('WORKER_INFRA_NAME', "micado_worker_infra")

clinet = docker.from_env()
run = False
i = 0
while not run and i < 5:
    try:
        run = True
        occopus = clinet.containers.get('occopus')
    except docker.errors.NotFound:
        run = False
        i += 1
        print("Occopus not running. Try {0} of 5.".format(i))
        time.sleep(5)

if run:
    result = occopus.exec_run("occopus-import {0}".format(node_def_file))
    print(result)
    if "Successfully imported" in result:
        print(occopus.exec_run("occopus-build --auth_data_path {0} -i {1} {2}".format(auth_data_file, worker_infra_name, infra_def_file)))
        print(requests.post("http://occopus:5000/infrastructures/{0}/attach".format(worker_infra_name)))
    else:
        print("Occopus import was unsuccessful!")
else:
    print ("Occopus not running!")