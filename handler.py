from client import MqttClient
import Adafruit_BBIO.GPIO as GPIO

def setup():
    GPIO.setup("USR3", GPIO.OUT)
    GPIO.setup("GPIO0_26", GPIO.OUT) # p1.34 as LED set to output

    # p1.20 set to GPIO input and pull up
    GPIO.setup("PRv0.16", GPIO.IN)
    GPIO.setup("PRv0.16", GPIO.PUD_UP)


def on_message_callback(client, userdata, message):
    # The received MQTT message is binary and must be decoded
    msg = message.payload.decode("utf-8")
    print(msg)
    if msg == "ON":
        GPIO.output("USR3", GPIO.HIGH)
        GPIO.output("GPIO0_26", GPIO.LOW)
    elif msg == "OFF":
        GPIO.output("USR3", GPIO.LOW)
        GPIO.output("GPIO0_26", GPIO.HIGH)
    else:
        print("No action taken!")


def handler_sub_main():
    # Define a subscriber that listens to all subjects
    subscriber = MqttClient("MessageHandler1", on_message_callback)

    # Only subscribe to relevant inbound messages
    subscriber.subscribe("mikroprojekt/inbound")

    print("Starting listening loop")
    subscriber.loop()

def handler_pub_main():
    #Sends off a single message and quits
    publisher = MqttClient("MessagePublisher", on_message_callback)
    publisher.publish("mikroprojekt/outbound", "OFF")

if __name__ == '__main__':
    setup()
    handler_sub_main()
