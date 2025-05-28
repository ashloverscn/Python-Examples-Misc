import paho.mqtt.client as mqtt
import json
import os
import datetime

# ─── MQTT Configuration ────────────────────────────────────────────────────────
MQTT_BROKER     = "e5122a5328ea4986a0295fa6e037655a.s2.eu.hivemq.cloud"
MQTT_PORT       = 8883
MQTT_USERNAME   = "admin"
MQTT_PASSWORD   = "admin1234S"
MQTT_TOPIC      = "#"  # Subscribe to all topics
CA_CERT_PATH    = "/etc/ssl/certs/ca-certificates.crt"  # Linux system CA

# ─── Output Directory ──────────────────────────────────────────────────────────
SDP_DIR = "sdp"
os.makedirs(SDP_DIR, exist_ok=True)

# ─── Utility: Clean SDP Formatting ─────────────────────────────────────────────
def clean_sdp(raw):
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8', errors='ignore')
    return raw.replace('\\r\\n', '\r\n').replace('\\n', '\n').strip()

# ─── Utility: Determine SDP Type ───────────────────────────────────────────────
def get_sdp_type(data):
    if isinstance(data, dict):
        return data.get("type", "unknown").lower()
    text = json.dumps(data).lower() if isinstance(data, dict) else str(data).lower()
    if "offer" in text:
        return "offer"
    elif "answer" in text:
        return "answer"
    elif "candidate" in text:
        return "candidate"
    return "unknown"

# ─── Utility: Save to File ─────────────────────────────────────────────────────
def save_sdp_to_file(sdp_type, content):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(SDP_DIR, f"{sdp_type}_{timestamp}.sdp")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 Saved {sdp_type.upper()} to: {filename}\n")

# ─── MQTT Callback: On Connect ─────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"❌ Connection failed with return code: {rc}")

# ─── MQTT Callback: On Message ─────────────────────────────────────────────────
def on_message(client, userdata, msg):
    print(f"\n📩 New message from topic: {msg.topic}")

    try:
        payload = msg.payload.decode('utf-8')
        try:
            data = json.loads(payload)
            sdp = data.get("sdp", payload)
        except json.JSONDecodeError:
            sdp = payload
            data = {}

        cleaned = clean_sdp(sdp)
        sdp_type = get_sdp_type(data)

        print(f"\n🧾 SDP TYPE: {sdp_type.upper()}")
        print("──────────────────────────────────────────────────────────────")
        print(cleaned)
        print("──────────────────────────────────────────────────────────────\n")

        save_sdp_to_file(sdp_type, cleaned)

    except Exception as e:
        print(f"⚠️ Error handling message: {e}")

# ─── Main Execution ────────────────────────────────────────────────────────────
def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set(ca_certs=CA_CERT_PATH)

    client.on_connect = on_connect
    client.on_message = on_message

    print("⏳ Connecting to MQTT broker...")
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()

# ─── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
