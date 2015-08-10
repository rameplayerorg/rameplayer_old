#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# Echo client program
import socket, time


def send_cmd(cmd):
	print cmd
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect("/tmp/lcd_server")
	s.send("display " + cmd)
	#data = s.recv(1024)
	#print data
	s.close()


send_cmd('lcd_server_test:Hello12345678901234567')
time.sleep(3)
send_cmd('display OK')


i=1

while(1):
	send_cmd("test:" + str(i));
	i = i + 1
	#time.sleep(0.5)
