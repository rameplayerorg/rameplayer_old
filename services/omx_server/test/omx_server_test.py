#!/usr/bin/env python
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# Echo client program
import socket, time


def send_cmd(cmd):
	print cmd
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect("/tmp/rameplayer")
	s.send(cmd)
	if(cmd=='ramecmd_status'):
		data = s.recv(1024)
		print "ramecmd_status:" + data
	s.close()


send_cmd('ramecmd_play /media/data/pk_FI_014_r720P.mp4')
send_cmd('ramecmd_status')
time.sleep(1)
send_cmd('ramecmd_status')
time.sleep(1)
send_cmd('ramecmd_status')
time.sleep(10)

send_cmd('ramecmd_pause')
time.sleep(1)
send_cmd('ramecmd_status')
time.sleep(10)

send_cmd('ramecmd_resume')
time.sleep(1)
send_cmd('ramecmd_status')
time.sleep(5)

send_cmd('ramecmd_stop')
time.sleep(1)
send_cmd('ramecmd_status')


send_cmd('ramecmd_play /media/data/test.mp4')
time.sleep(1)
send_cmd('ramecmd_status')
time.sleep(4)
