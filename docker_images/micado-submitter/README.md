# Micado submitter

Micado submitter for worker infrastructure descriptors

# Usage

The location of input template files and the created descriptor files can be set through these environment variables in the Docker Compose file:

* TEMP_AUTH_DATA_FILE
* TEMP_NODE_DEF_FILE
* TEMP_INFRA_DEF_FILE
* USER_DATA_FILE
* AUTH_DATA_FILE
* NODE_DEF_FILE
* INFRA_DEF_FILE

With the mounted volumes the occopus and the micado-submitter container can read and write these files.

The submitter takes the input parametres from the `USER_DATA_FILE` yaml file.

Limitations:
============
1. The submitter can prase only one:
    * Authentication information 
    * Node definition
    * Infra definition (scaling)
2. The submitter can start one infra and exit
3. More complex logging and exception handling are required

