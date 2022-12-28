"""
Book: Hands-On MQTT Programming with Python
Date : 27 Dec 22
"""
import os.path

# Not using tls certificate for MQTT
# however in the future need to look into this

mqtt_server_host = "192.168.2.99"
mqtt_server_port = 1883 # TLS is 8883
mqtt_keepalive = 120
