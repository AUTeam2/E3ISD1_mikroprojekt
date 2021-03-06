"""
This module implements a custome MQTT client, which can be of two types:
- Subscriber: Listens for messages on a given topic
- Publisher: Sends messages on a given topic
"""

import paho.mqtt.client as mqtt

class MqttClient():

    # These should be gotten from the environment ideally
    broker_address = "auteam2.mooo.com"
    broker_port = "1883"
    username = "team2"
    password = "team2"

    # This method is the same for all instances of the class
    @staticmethod
    def on_connect(client, userdata, flags, rc):
        #print("Connected with result code " + str(rc))
        pass

    # For outputting log messages to console
    @staticmethod
    def on_log(client, userdata, level, buf):
        pass
        #print("log: ", buf)

    # By default, do nothing on_message
    @staticmethod
    def on_message_default(client, userdata, message):
        pass

    #Initialize the client, straight on create
    def __init__(self, name, on_message, will_message="Logging off"):
        """ __init__ Handles all setup and connection when object is initialized.
        @:param: name is the name of the client, as will be shown on the server
        @:param: on_message is the callback used when this client receives a message
        @:param: will_message is the "Last Will" message sent when client loses conn
        """
        self.client = mqtt.Client(client_id=name,
                                    clean_session=True,
                                    userdata=None,
                                    transport="tcp")
        self.client.username_pw_set(MqttClient.username, MqttClient.password)
        self.client.on_connect = MqttClient.on_connect
        self.client.on_message = on_message

        # In production, let's consider disabling logging or routing to a file
        #self.client.on_log = MqttClient.on_log
        #self.client.enable_logger()

        # This ensures, that there is some sort of goodbye on losing connection
        self.client.will_set(name, will_message)

        # Connect immediately
        self.client.connect(MqttClient.broker_address)

    def publish(self, topic, payload):
        return self.client.publish(topic, payload)

    def subscribe(self, topic):
        return self.client.subscribe(topic)

    def loop(self):
        return self.client.loop_forever(retry_first_connection=False)

    def disconnect(self):
        return self.client.disconnect()
