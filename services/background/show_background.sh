#!/bin/bash
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# relates showing photo's in a player. Not needed while playing videos

BG_FILE="/media/data/background.jpg"

if [ -f $BG_FILE ];
then
   echo "Displaying background"
else
   echo "Displaying background: black"
   #echo "File $BG_FILE does not exists"
   BG_FILE="/home/pi/black.jpg"
fi


while pkill -0 fbi; do
	echo "fbi allready running, killing it first"
        sleep 0.5
	sudo pkill fbi
done


sudo fbi -T 2 -a -noverbose $BG_FILE
sleep 1
sudo pkill fbi

echo "Displaying background"
sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "Background"
