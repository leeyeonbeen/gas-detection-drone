import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("gasMeasure") 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if 10<float(msg.payload)<=30:
        GPIO.output(17, False)
        GPIO.output(18, True)
        time.sleep(0.3)
        GPIO.output(17, True)
        GPIO.output(18, False)
        time.sleep(0.3)
    elif 30<float(msg.payload)<=40:
        GPIO.output(17, False)
        GPIO.output(18, True)
        time.sleep(0.1)
        GPIO.output(17, True)
        GPIO.output(18, False)
        time.sleep(0.1)
    else:
        GPIO.output(17, False)
        GPIO.output(18, False)


client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 

client.connect("127.0.0.1", 1883, 60) 
client.loop_forever()
GPIO.output(17, False)
GPIO.output(18, False)