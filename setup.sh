#!/bin/bash
# RetroPi Control Install
CURRENT=`pwd`
PARENT=`dirname $CURRENT`
SCRIPTS='/home/pi/scripts'
#start install
echo "**************************************"
echo "Installing Pi Control"
echo "**************************************"
echo -n "**************************************"
echo -n "Warning!!! Installing the Pi Control Board on the incorrect pins on the Pi can damage your Pi!"
echo "Please use Pi Control Hardware and Software at your own risk. We do not take responsibility for any damages to your raspberry pi that may occure."
echo "By downloading and installing our hardware and software you are agreeing to these terms."
echo "**************************************"
echo -n "Would you like to continue with the installation? (y/n): "
read REPLY
if [ $REPLY = "y" ] || [ $REPLY = "Y" ]
then
    echo "**************************************"
    echo "Installing NFC Libraries and Webserver"
    apt-get install -y python-dev python-pip git
    git clone https://github.com/adafruit/Adafruit_Python_PN532.git
    cd Adafruit_Python_PN532
    python setup.py install
    cd ../
    rm -R Adafruit_Python_PN532
    pip install psutil
    pip install flask
    pip install flask-api
    pip install flask-httpauth
    #copy files
    echo "Installing Script Files...."
    mkdir -p $SCRIPTS/picontrol
    cp -r $PARENT/picontrol $SCRIPTS
    chmod -R 777 $SCRIPTS 
    echo "Enabling Serial Interface............."
    #echo 'enable_uart=1' >> /boot/config.txt
    sed -i '\:enable_uart=0:d' /boot/config.txt 
    sed -i '\:enable_uart=1:d' /boot/config.txt
    echo 'enable_uart=1' >> /boot/config.txt
    #update startup
    echo "Updating Startup Commands............."
    sed -i '\:emulationstation #auto:d' /opt/retropie/configs/all/autostart.sh
    sed -i '\:emulationstation:d' /opt/retropie/configs/all/autostart.sh
    sed -i '\:python /home/pi/scripts/picontrol/picontrol.py&:d' /opt/retropie/configs/all/autostart.sh
    echo 'python /home/pi/scripts/picontrol/picontrol.py&' >> /opt/retropie/configs/all/autostart.sh
    echo 'emulationstation' >> /opt/retropie/configs/all/autostart.sh
    rm -R /opt/retropie/configs/all/runcommand-onend.sh
    echo 'python /home/pi/scripts/picontrol/picontrol_gameend.py&' > /opt/retropie/configs/all/runcommand-onend.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onend.sh
    rm -R /opt/retropie/configs/all/runcommand-onstart.sh
    echo 'python /home/pi/scripts/picontrol/picontrol_gamestart.py&' > /opt/retropie/configs/all/runcommand-onstart.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onstart.sh
    echo "Installation Complete................."
    echo -n "You must reboot for changes to take effect, reboot now? (y/n): "
    read REPLY
    if [ $REPLY = "y" ] || [ $REPLY = "Y" ]
    then
        sudo reboot
    fi
fi
#end