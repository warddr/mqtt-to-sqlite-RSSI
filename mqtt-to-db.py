import paho.mqtt.client as mqtt
import sqlite3

conn = sqlite3.connect('rssi.db')
cursor = conn.cursor()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("AP/Sniffing/Device/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
 try:
    devid = (msg.topic.split("/")[3])
    bericht = (msg.payload.decode("utf-8").split("\r")[0].split("-"))
    rssi = bericht[1]
    hash = bericht[0]
    if (hash == "318876cd3585aa692733cbfe61afb5f539efa0f9ca9d60a9b6592aa20410dd11") : print(devid)
    cursor.execute("INSERT INTO rssi(dev_id, hash, rssi) VALUES (?,?,?)",(devid,hash,rssi))
    conn.commit()
 except:
    print("error, maar we gaan verder!");
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="IoT",password="DitIsGoed")
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


