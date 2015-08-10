#!/bin/bash
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# shows background image after boot


videomode="$(cfget -C /media/config/config.ini video/videomode)"
echo $videomode
sleep 20


BG_FILE="/media/data/background.jpg"

if [ -f $BG_FILE ];
then
   echo "File $BG_FILE exists"
else
   echo "File $BG_FILE does not exists"
   BG_FILE="/home/pi/black.jpg"
fi


#tvservice -e "CEA 19 HDMI"
#tvservice -e "CEA 31 HDMI"
#tvservice -e "$videomode"
#sleep 10

sudo fbi -T 2 -a -noverbose $BG_FILE
sudo fbi -T 2 -a -noverbose $BG_FILE
sleep 3
sudo pkill -9 fbi
