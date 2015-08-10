#!/bin/bash
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# mounts the USBs automatically and starts the GUI 

sleep 5
/usr/bin/sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "Init 30 sec"
/usr/bin/sudo mount /dev/sdb1 /media/data -o ro,uid=pi,gid=pi
sleep 25

file="/dev/sdb"
while echo looping; do
	if [ -e "$file" ]
	then
		echo "Found"
		sleep 2
		sudo mount /dev/sdb1 /media/data -o ro,uid=pi,gid=pi

		ps cax | grep gui.py > /dev/null
		if [ $? -eq 0 ]; then
			echo "gui.py is allready running."
		else
			echo "gui.py is not running. Starting it"
			/usr/bin/sudo /home/pi/gui.py &
		fi
	else
		echo "Not found"
		sleep 2
		/usr/bin/sudo umount /dev/sdb1
		/usr/bin/sudo pkill gui.py
		/usr/bin/sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "No USB Media"
	fi

done
