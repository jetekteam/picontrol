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

    #loop the button controls
    while True:
        try:
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
                    time.sleep(.5)
                    GPIO.output(gpioLed,1)
                    time.sleep(.5)
                    GPIO.output(gpioLed,0)
                    time.sleep(.5)
                    GPIO.output(gpioLed,1)
                    time.sleep(.5)
                    GPIO.output(gpioLed,0)
                    time.sleep(.5)
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

                        if (len(message.records) > 0):
                            gameData['console'] = message.records[0].value
                            gameData['rom'] = message.records[1].value


                    if gameData['console'] != '':
                        procs.runGame(gameData['console'], gameData['rom'], 'reset')
            #---------------------------------------------------------                
            if GPIO.input(gpioPower) == True:
                print('Shutting down now')
                os.system("sudo shutdown -h now")
        except:
            pass

        time.sleep(.10)

if __name__ == "__main__":
    main()
