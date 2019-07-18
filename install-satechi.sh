#!/bin/bash
# install script for TheOldPresbyope's moOde support of the
#   Satechi Bluetooth Multi-Media Remote
# code repo: https://github.com/theoldpresbyope/moode-satechi

read -p "Install Satechi support (y/n)? " answer
case ${answer:0:1} in
y|Y )
	echo "proceeding"	
;;
* )
	echo "exiting";
	exit 1
;;
esac

# copy files into final destination
sudo cp etc/udev/rules.d/42-satechi.rules /etc/udev/rules.d/42-satechi.rules
sudo cp etc/systemd/system/satechi.service /etc/systemd/system/satechi.service
sudo cp usr/local/bin/satechi.py /usr/local/bin/satechi.py

# ensure file permissions are correct
sudo chmod 644 /etc/udev/rules.d/42-satechi.rules
sudo chmod 644 /etc/systemd/system/satechi.service
sudo chmod 755 /usr/local/bin/satechi.py

read -p "Reboot now (y/n)? " answer
case ${answer:0:1} in
y|Y )
        echo "rebooting";
	sudo reboot
;;
* )
        echo "exiting";
        exit 1
;;
esac

