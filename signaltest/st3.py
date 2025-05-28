import paho.mqtt.client as mqtt
import json

# ─── MQTT Configuration ────────────────────────────────────────────────────────
MQTT_BROKER     = "e5122a5328ea4986a0295fa6e037655a.s2.eu.hivemq.cloud"
MQTT_PORT       = 8883  # Secure TLS Port
MQTT_USERNAME   = "admin"
MQTT_PASSWORD   = "admin1234S"
MQTT_TOPIC      = "#"  # Wildcard to listen to all topics
CA_CERT_PATH    = "/etc/ssl/certs/ca-certificates.crt"  # System CA root file

# ─── SDP Cleaning Function ─────────────────────────────────────────────────────
def clean_sdp(raw_sdp):
    """
    Convert escaped newline characters to actual newlines for readability.
    """
    if isinstance(raw_sdp, bytes):
        raw_sdp = raw_sdp.decode('utf-8', errors='ignore')
    cleaned = raw_sdp.replace('\\r\\n', '\r\n').replace('\\n', '\n').strip()
    return cleaned

# ─── MQTT Callback: On Connect ─────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected successfully to the MQTT broker.\n")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}\n")
    else:
        print(f"❌ Failed to connect. Return code: {rc}")

# ─── MQTT Callback: On Message ─────────────────────────────────────────────────
def on_message(client, userdata, msg):
    print(f"🔔 Incoming Message on Topic: {msg.topic}")

    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        sdp = data.get('sdp', payload)
    except json.JSONDecodeError:
        sdp = payload
    except Exception as e:
        print(f"⚠️ Error parsing message: {e}")
        return

    cleaned_sdp = clean_sdp(sdp)

    print("\n🧾 Extracted & Cleaned SDP Offer:\n")
    print("="*60)
    print(cleaned_sdp)
    print("="*60 + "\n")

# ─── Main MQTT Initialization ─────────────────────────────────────────────────
def main():
    client = mqtt.Client()

    # Set login credentials
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Enable TLS encryption using system certificates
    client.tls_set(ca_certs=CA_CERT_PATH)

    # Attach callback handlers
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect and loop forever
    print("⏳ Connecting to the MQTT broker...\n")
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

# ─── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
