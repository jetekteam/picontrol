#!/bin/bash
# RetroPi Control Install

if [[ $EUID > 0 ]]; then # we can compare directly with this syntax.
  echo "Please run as root/sudo"
  exit 1
fi

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
    echo "Installing Webserver and Scripts"
    apt-get update
    apt-get install -y python-dev python-pip git
    pip install picontrol

    #copy files
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
    sed -i '\:pic_control&:d' /opt/retropie/configs/all/autostart.sh
    echo 'pic_control&' >> /opt/retropie/configs/all/autostart.sh
    echo 'emulationstation' >> /opt/retropie/configs/all/autostart.sh
    rm -R /opt/retropie/configs/all/runcommand-onend.sh
    echo 'pic_gameend&' > /opt/retropie/configs/all/runcommand-onend.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onend.sh
    rm -R /opt/retropie/configs/all/runcommand-onstart.sh
    echo 'pic_gamestart&' > /opt/retropie/configs/all/runcommand-onstart.sh
    chmod -R 7777 /opt/retropie/configs/all/runcommand-onstart.sh

    echo "Installation Complete................."
    echo -n "You must reboot for changes to take effect, reboot now? (y/n): "
    read REPLY
    if [ $REPLY = "y" ] || [ $REPLY = "Y" ]
    then
        reboot
    fi
fi
#end
