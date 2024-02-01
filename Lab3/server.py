import paho.mqtt.client as mqtt
import rps_ai as rps

client1_input = None
client2_input = None

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/lab3/client1", qos=1)
    client.subscribe("ece180d/lab3/client2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print(message.topic)
    if message.topic == "ece180d/lab3/client1":
        global client1_input
        client1_input = message.payload.decode()
    elif message.topic == "ece180d/lab3/client2":
        global client2_input
        client2_input = message.payload.decode()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async('mqtt.eclipseprojects.io')

client.loop_start()

while True:
    if client1_input and client2_input:
        message = f"Player1 played {client1_input} and Player2 played {client2_input}. {rps.get_winner(client1_input, client2_input, True)}"
        client.publish("ece180d/lab3/server", message)
        client1_input = None
        client2_input = None

# State where waiting for client inputs 