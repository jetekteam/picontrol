import sys, os, time, json, subprocess
import RPi.GPIO as GPIO
from picontrol import processes as procs
from picontrol import nfc
from picontrol import ndef

def main():
    #setup GPIO
    gpioPower = 3
    gpioReset = 23
    gpioLed = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #setup the power button
    GPIO.setup(gpioPower, GPIO.IN, GPIO.PUD_UP)
    #setup the reset button
    GPIO.setup(gpioReset, GPIO.IN, GPIO.PUD_UP)
    #setup the led
    GPIO.setup(gpioLed, GPIO.OUT)
    GPIO.output(gpioLed,1)

    shutDownCounter = 0

    #loop the button controls
    while True:
        try:
            # check if we turned the power button off, if we did lets see if we turned it back on to load a game
            if shutDownCounter > 0:
                gameData = {'console':'', 'rom':''}
                if GPIO.input(gpioPower) == False:
                    # try to load the nfc tag
                    response = nfc.read()

                    if response.type == 'success':
                        #we have a cart in the console
                        message = response.data

                        if (len(message.records) > 0):
                            gameData['console'] = message.records[0].value
                            gameData['rom'] = message.records[1].value

                        #start game
                        procs.runGame(gameData['console'], gameData['rom'], 'nfc')
                    else:
                        #start es
                        procs.runGame('', '', '')

            if GPIO.input(gpioPower) == True:
                # turn off led
                GPIO.output(gpioLed,0)

                # we hit the power button, kill running game or es
                procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                        "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                        "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                        "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                        "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                        "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                        "wolf4sdl", "solarus", "emulationstation"]
                procs.killTasks(procnames)

                shutDownCounter += 1

                if shutDownCounter >= 175:
                    shutDownCounter = 0

                    GPIO.output(14,1)
                    time.sleep(0.5)
                    GPIO.output(14,0)
                    time.sleep(0.5)
                    GPIO.output(14,1)
                    time.sleep(0.5)
                    GPIO.output(14,0)
                    time.sleep(0.5)
                    GPIO.output(14,1)
                    time.sleep(0.5)
                    GPIO.output(14,0)

                    print('Shutting down now')
                    os.system("sudo shutdown -h now")
            else:
                if shutDownCounter > 0:
                    GPIO.output(gpioLed,1)
                    shutDownCounter = 0
            #---------------------------------------------------------  
            if shutDownCounter == 0:
                if GPIO.input(gpioReset) == False:
                    writeNFC = False
                    timer = 0
                    # we held the reset button then we want to write to the nfc, else we reset the rom
                    while timer < 2.0:
                        if GPIO.input(gpioReset) == False:
                            writeNFC = True
                        else:
                            writeNFC = False
                            break
                        timer += .1
                        time.sleep(.1)

                    # get the current game info and write it to the nfc
                    gameData = {'console':'','rom':''}
                    content = []
                    try:
                        with open('/dev/shm/runcommand.info') as f:
                            content = f.readlines()

                        filename = content[2]
                        gameData['console'] = content[0].replace('\n','')
                        gameData['rom'] = filename.rpartition('/')[2].replace('\n','')

                    except:
                        pass

                    if writeNFC == True:
                        GPIO.output(gpioLed,0)
                        time.sleep(0.5)
                        GPIO.output(gpioLed,1)
                        time.sleep(0.5)
                        GPIO.output(gpioLed,0)
                        time.sleep(0.5)
                        GPIO.output(gpioLed,1)
                        time.sleep(0.5)
                        GPIO.output(gpioLed,0)
                        time.sleep(0.5)
                        GPIO.output(gpioLed,1)

                        message = ndef.Message()
                        message.addTextRecord(gameData['console'])
                        message.addTextRecord(gameData['rom'])

                        response = nfc.write(message)
                    else:
                        GPIO.output(gpioLed,0)
                        time.sleep(.5)
                        GPIO.output(gpioLed,1)

                        # try reading from nfc first...
                        response = nfc.read()

                        if response.type == 'success':
                            #we have a cart in the console
                            message = response.data
                            gameData['console'] = message.records[0].value
                            gameData['rom'] = message.records[1].value


                        if gameData['console'] != '':
                            procs.runGame(gameData['console'], gameData['rom'], 'reset'

        except:
            pass

        time.sleep(0.1)

if __name__ == "__main__":
    main()
