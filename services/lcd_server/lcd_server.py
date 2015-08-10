#!/usr/bin/env python
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# Handle's LCD operations
#
import dbus, time, pipes, socket,os
from subprocess import Popen


def display(message):

	print "display handler: " + message

	if (len(message) > 16):
		row1 = message[0:16]
		row2 = message[16:]
	else:
		row1=message
		row2=""

        row1=row1+"                 "
        row2=row2+"                 "

        row1 = row1.replace("-", "_")
        row2 = row2.replace("-", "_")

        command="/home/pi/lcdi2c -b 1 -x 0 -y 0 \"" + row1[0:16] + "\""
        print command
        os.system( command  )
        command="/home/pi/lcdi2c -b 1 -x 0 -y 1 \"" + row2[0:16] + "\""
        print command
        os.system( command  )



socket_file="/tmp/lcd_server"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
        os.remove(socket_file)
except OSError:
        pass

s.bind(socket_file)
os.chmod(socket_file, 0o777);


os.system("/home/pi/lcdi2c -i -b 1")
while 1:

	s.listen(1)
	print "starting to listen /tmp/rame/lcd_server"

	conn, addr = s.accept()
	print "client connected"
	while 1:
        	data = conn.recv(1024)
        	if not data:
			break

		print data
		#print "pos" + str(data.find("display"))
		if(data.find("display")==0):
			display(data[8:])

        	#conn.send(data)
        	print data

	conn.close()
