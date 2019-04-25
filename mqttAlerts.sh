#! /bin/bash


SCRIPT_PATH=`dirname "${BASH_SOURCE[0]}"`
source $SCRIPT_PATH/../venvs/mqttAlerts/bin/activate
echo `type python3.7`

exec $SCRIPT_PATH/mqttAlerts.py
