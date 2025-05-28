import paho.mqtt.client as mqtt
import ssl

# MQTT connection details
MQTT_BROKER = "e5122a5328ea4986a0295fa6e037655a.s2.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "admin"
MQTT_PASSWORD = "admin1234S"
MQTT_TOPIC = "#"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic '{MQTT_TOPIC}'")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

def on_log(client, userdata, level, buf):
    # Mimic mosquitto_sub -d debug output
    print(f"Log: {buf}")

def main():
    client = mqtt.Client()

    # Set username and password
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Enable TLS with TLSv1.2
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)

    # Set debug log callback to mimic -d
    client.on_log = on_log

    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to broker
    client.connect(MQTT_BROKER, MQTT_PORT)

    # Blocking loop to process network traffic and dispatch callbacks
    client.loop_forever()

if __name__ == "__main__":
    main()
