#! /usr/bin/env python3.7
"""
when an mqtt topic meets a specific condition as defined in the
configuration file, the alert function for the plugin is called
with: 

    source is a string with the mqtt topic that triggered the 
    alert

    condition is a string with the reason the alert was 
    triggered

    notify is a string with the value from the notify value 
    from the configuration file
"""


from pluginbase import PluginBase
from configparser import ConfigParser
import os
import paho.mqtt.client as mqtt


class Alert(object):
    def __init__(self, name, config, plugin):
        self.name = name
        self.config = config
        self.topic = self.config.get('topic')
        self.plugin = plugin
        self.alert = plugin.alert
        self.setup = plugin.setup
        self.setup(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


config = ConfigParser()
ini_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mqttAlerts.ini')
config.read(ini_file)
alerts = {}

plugin_base = PluginBase(package='.plugins')
plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins',])
plugins_loaded = {}

alert_configs = [item[1] for item in config.items() if item[0].startswith("alert")]

for alert_config in alert_configs:
    #print(alert_config)

    alert_name = alert_config.name
    plugin_name = alert_config.get('plugin')
    try:
        plugin = plugins_loaded[plugin_name]

    except KeyError:
        plugins_loaded[plugin_name] = plugin_source.load_plugin(plugin_name)
        plugin = plugins_loaded[plugin_name]
        print(f'{plugin.name} loaded')

    alerts[alert_name] = Alert(alert_name, alert_config, plugin)

print(alerts)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    topics = list(set([(userdata[a].topic, 0) for a in userdata]))

    print(topics)

    rc = client.subscribe(topics)
    print(f'subscribe result: {rc}')


def on_message(client, userdata, msg):
    print(f'{msg.topic} {msg.payload}')


client = mqtt.Client(userdata = alerts)
client.on_connect = on_connect
client.on_message = on_message

mqtt_host = config.get('mqtt', 'host')
mqtt_port = config.getint('mqtt', 'port')
print(f'connecting to {mqtt_host} on port {mqtt_port}')

client.connect(mqtt_host, mqtt_port, 60)
client.loop_forever()
