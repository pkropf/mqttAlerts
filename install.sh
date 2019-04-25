#! /bin/bash


cp -b -S "-`date "+%Y%m%d%H%M%S"`" mqttAlerts.ini     /usr/local/bin/
cp mqttAlerts.py      /usr/local/bin/
cp mqttAlerts.sh      /usr/local/bin/
cp mqttAlerts.service /lib/systemd/system/

systemctl daemon-reload
systemctl enable mqttAlerts
systemctl start mqttAlerts
