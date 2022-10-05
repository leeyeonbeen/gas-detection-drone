import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

cnt1=0
cnt2=0
cnt3=0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("gasMeasure") 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if 10<float(msg.payload)<=20:
        cnt1+=1
        cnt2=0
        cnt3=0
        if cnt1<=3:
            GPIO.output(26, True)
        elif cnt<=6:
            GPIO.output(26, False)
            if cnt1==6:
                cnt1=0
    elif 20<float(msg.payload)<=30:
        cnt2+=1
        cnt1=0
        cnt3=0
        if cnt2<=2:
            GPIO.output(26, True)
        elif cnt2<=4:
            GPIO.output(26, False)
            if cnt2==4:
                cnt2=0
    elif 30<float(msg.payload)<=40:
        cnt3+=1
        cnt1=0
        cnt2=0
        if cnt3==1:
            GPIO.output(26, True)
        elif cnt3==2:
            GPIO.output(26, False)
            cnt3=0

client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 

client.connect("127.0.0.1", 1883, 60) 
client.loop_forever()

GPIO.cleanup()
GPIO.output(26, False)