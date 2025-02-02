import network
import time
from machine import Pin
from utime import sleep
from umqtt.simple import MQTTClient
import ujson

# Inisialisasi LED
led = Pin(2, Pin.OUT)
led2 = Pin(15, Pin.OUT)

# Konfigurasi Wi-Fi
WIFI_SSID = ""
WIFI_PASSWORD = ""

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...")
    for i in range(10):
        if wlan.isconnected():
            print("Connected to Wi-Fi!")
            print(f"IP Address: {wlan.ifconfig()[0]}")
            return wlan
        time.sleep(1)
    raise RuntimeError("Failed to connect to Wi-Fi")

# Hubungkan ke Wi-Fi
try:
    wifi = connect_wifi(WIFI_SSID, WIFI_PASSWORD)
except RuntimeError as e:
    print(e)
    while True:
        pass

# Parameter MQTT
MQTT_CLIENT_ID = "micropython-Esp32-PK"
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = ""

# Koneksi ke server MQTT
print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

# Fungsi callback untuk menerima pesan
def sub_cb(topic, msg):
    try:
        message = ujson.loads(msg)
        print(f"Received message on topic {topic.decode()}: {message}")
        if message.get("msg") == "ON":
            print("Turning LED ON")
            led.on()
            led2.off()
        elif message.get("msg") == "OFF":
            print("Turning LED OFF")
            led.off()
            led2.on()
    except Exception as e:
        print(f"Error parsing message: {e}")

# Subskripsi ke topik
client.set_callback(sub_cb)
client.subscribe(MQTT_TOPIC)
print(f"Subscribed to topic {MQTT_TOPIC}")

# Loop utama
try:
    while True:
        client.check_msg()
        sleep(0.1)
except KeyboardInterrupt:
    print("Disconnected from MQTT broker.")
    client.disconnect()