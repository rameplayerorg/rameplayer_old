#!/bin/sh
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# 5s after boot copies the network config to RAM and restarts the service
sleep 5
sudo cp /media/config/interfaces /etc/network/interfaces
sudo cp /media/config/dnsmasq.conf /etc/dnsmasq.conf
sudo service networking restart
sudo service dnsmasq restart
