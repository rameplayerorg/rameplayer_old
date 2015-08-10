#!/bin/sh
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
#/usr/bin/sudo /home/pi/lcdi2c -i -b 1 -x 0 -y 0 "Init 30sec"
#echo "waiting 20 seconds for netconfig"
#sleep 30
/usr/bin/sudo /home/button_server/button_server.py
