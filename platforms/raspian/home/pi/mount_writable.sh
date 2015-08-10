#!/bin/bash
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# reopen SD card and USB sticks for writing
#

sudo mount -o remount,rw /alpine
sudo mount -o remount,rw /boot
sudo mount -o remount,rw /
sudo mount -o remount,rw /media/config
sudo mount -o remount,rw /media/data
