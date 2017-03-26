#!/usr/bin/env python
import RPi.GPIO as GPIO
import os, time, ConfigParser

gpioFan = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioFan, GPIO.OUT)

fan_on = False

def getCPUtemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return (res.replace("temp=","").replace("'C\n",""))

def getConfig():
    config = ConfigParser.RawConfigParser()
    configFilePath = r'/home/pi/scripts/picontrol/configs/config.conf'
    config.read(configFilePath)
    return config

while True:
    config = getConfig()
    thresholdOn = 60
    thresholdOff = 55
    interval_value = 30

    try:
        thresholdOn = int(config.get("fan", "thresholdOn"))    
        thresholdOff = int(config.get("fan", "thresholdOff"))    
        interval = float(config.get("fan", "interval")) 
    except:
	    print 'unable to access config file'

    temp = int(float(getCPUtemp()))
    if temp >= thresholdOn:
        GPIO.output(gpioFan,1)
        fan_on = True      
    else:
	    if (fan_on == True & temp <= thresholdOff - 5):
		    GPIO.output(gpioFan,0)

    time.sleep(float(interval))
