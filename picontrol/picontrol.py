import sys, os, time, json, subprocess, ConfigParser
import RPi.GPIO as GPIO
from picontrol import processes as procs
from picontrol import nfc
import picontrol.config


def main():
    #start fan
    os.system('pkill -9 -f pic_fan')
    subprocess.Popen('pic_fan&', shell=True)

    #start webserver
    os.system('pkill -9 -f pic_web')
    os.system('sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 8080')
    subprocess.Popen('pic_web&', shell=True)

    #get button option and start the process
    os.system('pkill -9 -f pic_button_pi')
    os.system('pkill -9 -f pic_button_classic')
    config = picontrol.config.load_config()
    buttonOption = int(config.get("button", "option"))

    if buttonOption == 1:
        subprocess.Popen('pic_button_classic&', shell=True)
    else:
        subprocess.Popen('pic_button_pi&', shell=True)

    #check if we have a tag inserted and boot that game
    response = nfc.read()

    if response.type == 'success':
        message = response.data
        procs.runGame(message.records[0].value, message.records[1].value, 'nfc')

if __name__ == "__main__":
    main()
