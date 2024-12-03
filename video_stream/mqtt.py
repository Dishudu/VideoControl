import paho.mqtt.client as mqtt
from django.conf import settings

def send_relay_command(command):
    client = mqtt.Client()
    try:
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
    client.publish("esp8266/relay", command)
    client.disconnect()

