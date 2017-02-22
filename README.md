# Pi Control
-----------------
## Pi Control Install 
(Requires RetroPie, please see instructions to install RetroPie at https://retropie.org.uk)

1. Configure keyboard if not already done
  * up, down, left, right, start, select, a, and b are enough for now
2. In settings, connect to local network, choose “SHOW IP” and make a note of the IP address given to your Pi.
3. Press F4 on the keyboard to exit to the terminal.
4. Download Pi Control archive by typing:
  * wget https://github.com/jetechfiles/picontrol/raw/master/picontrol.tgz
5. Extract archive by typing:
  * tar -xzf picontrol.tgz
6. Change directory by typing:
  * cd picontrol
7. Run setup(Could take several minutes, depending on network speeds) by typing:
  * sudo sh ./setup.sh
8. When prompted to reboot type “y” and hit enter.
9. After reboot you may now access Pi Control web app from any browser connected to same local network by typing in the IP address of the Pi.
  * Example: 192.168.1.25
  * Default Username: picontrol
  * Default Password: password
