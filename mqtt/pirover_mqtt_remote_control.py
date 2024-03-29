"""
Book: Hands-On MQTT Programming  with Python
Date: 27 Dec 2022
"""
from config import *
from pirover_commands import *
import paho.mqtt.client as mqtt
import time
import json

vehicle_name = "pirover01"
commands_topic = "vehicles/{}/commands".format(vehicle_name)
processed_commands_topic = "vehicles/{}/executedcommands".format(vehicle_name)

class LoopControl:
    is_last_command_processed = False

def on_connect(client, userdata, flags, rc):
    print("result from connect: {}".format(
        mqtt.connack_string(rc)))
    # Check whether the result from connect is the CONNACK_ACCEPTED connack code
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to the commands topic filter
        client.subscribe(
            processed_commands_topic,
            qos=2)


def on_message(client, userdata, msg):
    if msg.topic == processed_commands_topic:
        print(str(msg.payload))
        if str(msg.payload).count(CMD_TURN_OFF_ENGINE) > 0:
            LoopControl.is_last_command_processed = True

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def build_command_message(command_name, key="", value=""):
    if key:
        # The command requires a key
        command_message = json.dumps({COMMAND_KEY: command_name, key: value})
    else:
        # The command doesn't require a key
        command_message = json.dumps({COMMAND_KEY: command_name})
    return command_message

def publish_command(client, command_name, key="", value=""):
    command_message = build_command_message(command_name, key, value)
    result = client.publish(topic=commands_topic, payload=command_message, qos=2)
    client.loop()
    time.sleep(1)
    return result

if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(host=mqtt_server_host,
        port=mqtt_server_port,
        keepalive=mqtt_keepalive)
    publish_command(client, CMD_SET_MAX_SPEED, KEY_MPH, 30)
    publish_command(client, CMD_SET_MIN_SPEED, KEY_MPH, 8)
    publish_command(client, CMD_LOCK_DOORS)
    publish_command(client, CMD_TURN_ON_ENGINE)
    # publish_command(client, CMD_ROTATE_RIGHT, KEY_DEGREES, 15)
    # publish_command(client, CMD_ACCELERATE)
    # publish_command(client, CMD_ROTATE_RIGHT, KEY_DEGREES, 25)
    # publish_command(client, CMD_ACCELERATE)
    # publish_command(client, CMD_ROTATE_LEFT, KEY_DEGREES, 15)
    # publish_command(client, CMD_ACCELERATE)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_RIGHT)
    publish_command(client, CMD_PAN_LEFT)
    publish_command(client, CMD_PAN_LEFT)
    publish_command(client, CMD_PAN_LEFT)
    publish_command(client, CMD_PAN_LEFT)
    publish_command(client, CMD_PAN_LEFT)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_UP)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TILT_DOWN)
    publish_command(client, CMD_TURN_OFF_ENGINE)
    while LoopControl.is_last_command_processed == False:
        # Process messages and the commands every 500 milliseconds
        client.loop()
        time.sleep(0.5)
    client.disconnect()
    client.loop()
    
