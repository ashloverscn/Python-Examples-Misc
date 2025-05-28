import paho.mqtt.client as mqtt
import json

# MQTT connection parameters from your config
MQTT_BROKER = "e5122a5328ea4986a0295fa6e037655a.s2.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "admin"
MQTT_PASSWORD = "admin1234S"
MQTT_TOPIC = "#"  # subscribe to all topics, or change to your specific topic

# Path to CA cert - HiveMQ Cloud uses standard trusted CA, so you can also skip this on many systems
CA_CERT_PATH = "/etc/ssl/certs/ca-certificates.crt"

def clean_sdp(raw_sdp):
    if isinstance(raw_sdp, bytes):
        raw_sdp = raw_sdp.decode('utf-8', errors='ignore')
    # Replace escaped newlines with real newlines
    cleaned = raw_sdp.replace('\\r\\n', '\r\n').replace('\\n', '\n').strip()
    return cleaned

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully.")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"\n--- New message on topic: {msg.topic} ---")
    try:
        payload = msg.payload.decode('utf-8')
        # Attempt to parse JSON to extract SDP if present
        try:
            data = json.loads(payload)
            sdp = data.get('sdp', payload)  # fallback to entire payload if no 'sdp' key
        except json.JSONDecodeError:
            sdp = payload

        cleaned_sdp = clean_sdp(sdp)
        print("Cleaned SDP:\n")
        print(cleaned_sdp)
        print("--- End of SDP ---\n")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set(ca_certs=CA_CERT_PATH)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

if __name__ == "__main__":
    main()
