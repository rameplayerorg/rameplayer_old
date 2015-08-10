#!/bin/sh
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# For reference ONLY! Not in USE!

#sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "Displaying image"
pkill omxplayer
sudo fbi -T 2 -noverbose -a $1
sleep 1
sudo pkill fbi
