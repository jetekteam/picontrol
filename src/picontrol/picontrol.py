import sys, os, time, json, subprocess, ConfigParser
import RPi.GPIO as GPIO
import picontrol_processes as procs
import picontrol_nfc as nfc
import picontrol_ndef as ndef

def getConfig():
    config = ConfigParser.RawConfigParser()
    configFilePath = r'/home/pi/scripts/picontrol/configs/config.conf'
    config.read(configFilePath)
    return config

#start fan
os.system('pkill -9 -f picontrol_fan.py')
subprocess.Popen('python /home/pi/scripts/picontrol/picontrol_fan.py&', shell=True)

#start webserver
os.system('pkill -9 -f picontrol_web.py')
os.system('sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 8080')
subprocess.Popen('python /home/pi/scripts/picontrol/webserver/picontrol_web.py&', shell=True)

#get button option and start the process
os.system('pkill -9 -f picontrol_button_pi.py')
os.system('pkill -9 -f picontrol_button_classic.py')
config = getConfig()
buttonOption = int(config.get("button", "option")) 

if buttonOption == 1:
    subprocess.Popen('python /home/pi/scripts/picontrol/picontrol_button_classic.py&', shell=True)
else:
    subprocess.Popen('python /home/pi/scripts/picontrol/picontrol_button_pi.py&', shell=True)    

#check if we have a tag inserted and boot that game
response = nfc.read()
            
if response.type == 'success':
    message = response.data
    procs.runGame(message.records[0].value, message.records[1].value, 'nfc')