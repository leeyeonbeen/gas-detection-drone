#!/usr/bin/python

import time
import random
import os
import RPi.GPIO as GPIO
import requests
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
time.time()
GPIO.setwarnings(False)

mqtt = mqtt.Client("python_pub") 
mqtt.connect("127.0.0.1", 1883) 

#=========================================================

#1st sensor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#2nd sensor
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

result_f = ""
result_r = ""

#======================================================

def front_sensors(FA, FB):
    global result_f
    if ((FA==0)&(FB==0)):
        result_f = random.randrange(0,10)
    elif ((FA==0)&(FB==1)):
        result_f = random.randrange(10,20)
    elif ((FA==1)&(FB==0)):
        result_f = random.randrange(20,30)
    elif ((FA==1)&(FB==1)):
        result_f = random.randrange(30,40)
    return result_f

def rear_sensors(RA, RB):
    global result_r
    if ((RA==0)&(RB==0)):
        result_r = random.randrange(0,10)
    elif ((RA==0)&(RB==1)):
        result_r = random.randrange(10,20)
    elif ((RA==1)&(RB==0)):
        result_r = random.randrange(20,30)
    elif ((RA==1)&(RB==1)):
        result_r = random.randrange(30,40)
    return result_r

def db_update(default_m, front_m, rear_m):
    url_string = '{url_string}'
    data_string_1 = "gasdb,host=drone default_m={}".format(default_m)
    data_string_2 = "gasdb,host=drone front_m={}".format(front_m)
    data_string_3 = "gasdb,host=drone rear_m={}".format(rear_m)
    
    r1 = requests.post(url_string, data=data_string_1)
    r2 = requests.post(url_string, data=data_string_2)
    r3 = requests.post(url_string, data=data_string_3)
    mqtt.publish("gasMeasure", front_m+rear_m/2)
    return True 

#==========================================================

try:
    while True:     
        FA = (GPIO.input(27))
        FB = (GPIO.input(22))
        RA = (GPIO.input(23))
        RB = (GPIO.input(24))

        default_m=10
        front_m=front_sensors(FA, FB)
        rear_m=rear_sensors(RA, RB)

        db_update(default_m, front_m, rear_m)
        time.sleep(1.0)
 
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    
except:
    print("Wrong key, Some error")
        
finally:
    print("Clean Up")
    GPIO.cleanup()