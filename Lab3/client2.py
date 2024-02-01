import paho.mqtt.client as mqtt
import rps_ai as rps

input_sent = False

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # subscribe to game server
    client.subscribe("ece180d/lab3/server", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    result = message.payload.decode()
    global input_sent
    input_sent = False
    print(result)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')

client.loop_start()

while True:
    if input_sent == False:
        user_input = rps.get_user_input()
        client.publish("ece180d/lab3/client2", user_input)
        input_sent = True