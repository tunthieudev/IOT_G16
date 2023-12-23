import paho.mqtt.client as paho
from paho import mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


class Connection:
    def __init__(self):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set("tuanvp34", "Tuan3402")
        self.client.connect("7ec23135bbf94e7599fa8e9a5a7ec748.s2.eu.hivemq.cloud", 8883)

        self.client.on_subscribe = on_subscribe
        self.client.on_message = on_message
        self.client.on_publish = on_publish

        self.client.loop_start()

    def public(self, topic, message):
        self.client.publish(topic, message, qos=1)

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=1)
