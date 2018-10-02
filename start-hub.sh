#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update &&
apt-get install -y python-pip &&
pip install azure-cli applicationinsights &&
pip install azure-batch &&
pip install azure-mgmt-storage &&
pip install setuptools && 
pip install azure &&
pip install configparser &&

mkdir /usr/monitor
chmod 755 /usr/monitor
cp monitor.py /usr/monitor/monitor.py
chmod 755 /usr/monitor/monitor.py

PARAM_FILE=/usr/monitor/monitor.cfg
echo "[DEFAULT]" > $PARAM_FILE
echo "AZURE_SUBSCRIPTION_ID=$1" >> $PARAM_FILE
echo "AZURE_CLIENT_ID=$2" >> $PARAM_FILE
echo "AZURE_CLIENT_SECRET=$3" >> $PARAM_FILE
echo "AZURE_TENANT_ID=$4" >> $PARAM_FILE
echo "PANORAMA_IP=$5" >> $PARAM_FILE
echo "PANORAMA_API_KEY=$6" >> $PARAM_FILE
echo "LICENSE_DEACTIVATION_API_KEY=$7" >> $PARAM_FILE
echo "RG_NAME=$8" >> $PARAM_FILE
echo "WORKER_NAME=$9" >> $PARAM_FILE
echo "VMSS_NAME=$10" >> $PARAM_FILE
echo "APPINSIGHTS_NAME=$11" >> $PARAM_FILE

./publish.py &&
sleep 60 &&

crontab -l > _tmp_file
echo "*/5 * * * * /usr/monitor/monitor.py" >> _tmp_file
crontab _tmp_file
