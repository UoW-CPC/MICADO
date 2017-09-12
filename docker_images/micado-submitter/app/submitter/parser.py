#!/usr/bin/env python
import os
import ruamel.yaml as YAML

yaml = YAML
yaml.default_flow_style = False


def set_auth_data(temp_data, user_data, index, attribute):
    temp_data.get("resource")[index].get("auth_data")[attribute] = user_data.get("user_data").get("auth_data").get(
        attribute)


def generate_auth_data(user_data, temp_auth_data):
    if user_data.get("user_data").get("auth_data").get("type") == "ec2":
        i = 0
        while temp_auth_data.get("resource")[i].get("type") != "ec2":
            i += 1
        set_auth_data(temp_auth_data, user_data, i, "accesskey")
        set_auth_data(temp_auth_data, user_data, i, "secretkey")

    elif user_data.get("user_data").get("auth_data").get("type") == "nova":
        i = 0
        while temp_auth_data.get("resource")[i].get("type") != "nova":
            i += 1
        set_auth_data(temp_auth_data, user_data, i, "username")
        set_auth_data(temp_auth_data, user_data, i, "password")

    elif user_data.get("user_data").get("auth_data").get("type") == "occi":
        i = 0
        while temp_auth_data.get("resource")[i].get("type") != "occi":
            i += 1
        set_auth_data(temp_auth_data, user_data, i, "proxy")

    elif user_data.get("user_data").get("auth_data").get("type") == "cloudbroker":
        i = 0
        while temp_auth_data.get("resource")[i].get("type") != "cloudbroker":
            i += 1
        set_auth_data(temp_auth_data, user_data, i, "email")
        set_auth_data(temp_auth_data, user_data, i, "password")

    elif user_data.get("user_data").get("auth_data").get("type") == "cloudsigma":
        i = 0
        while temp_auth_data.get("resource")[i].get("type") != "cloudsigma":
            i += 1
        set_auth_data(temp_auth_data, user_data, i, "email")
        set_auth_data(temp_auth_data, user_data, i, "password")


def generate_node_def(user_data, temp_node_def):
    temp_node_def.get("node_def:worker")[0]["resource"] = user_data.get("user_data").get("resource")


def generate_infra_def(user_data, temp_infra_def):
    temp_infra_def.get('nodes')[0].get('scaling')['min'] = user_data.get('user_data').get('scaling').get('min')
    temp_infra_def.get('nodes')[0].get('scaling')['max'] = user_data.get('user_data').get('scaling').get('max')
    temp_infra_def.get('variables')['master_host_ip'] = os.getenv('MASTER_IP', '127.0.0.1')