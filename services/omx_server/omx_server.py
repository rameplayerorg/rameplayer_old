#!/usr/bin/env python
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# Wrapper for omxplayer DBUS communication

import dbus, time, pipes, socket, os, commands
from subprocess import Popen
from dbus.mainloop.glib import DBusGMainLoop


DBusGMainLoop(set_as_default=True)


state="run"

dbusIfaceProp = None
dbusIfaceKey = None
omxprocess = None

# Get devicename from configfile
audioport=commands.getoutput("/usr/bin/cfget -C /media/config/config.ini mediaplayer/audioport")
print "audioport:" + audioport


def handler(sender=None):
    print "!!!!!!!!!!!!1 got signal from %r !!!!!!!!!!!!!!!!!1" % sender


def display_lcd(cmd):
        print "display_lcd:" + cmd
	try:
	        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        	s.connect("/tmp/lcd_server")
	        s.send("display " + cmd)
        	s.close()
	except:
		print "display_lcd failed"

def play(file):
	global dbusIfaceProp, dbusIfaceKey, omxprocess, audioport

	print "play handler: "+ file

	# media file to open
	#file="/media/data/test.mp4"

	# open omxplayer
	cmd = "/usr/bin/omxplayer  --no-osd -o" + audioport + " %s" %(file)
	omxprocess = Popen([cmd], shell=True)

	# wait for omxplayer to initialise
	done,retry=0,0
	while done==0:
	    	try:
        		with open('/tmp/omxplayerdbus.root', 'r+') as f:
            			omxplayerdbus = f.read().strip()
	        	bus = dbus.bus.BusConnection(omxplayerdbus)
        		object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
        		dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
	        	dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
			done=1
	    	except Exception,e:
        		retry+=1
			time.sleep(0.1)
        		if retry >= 20000:
				print str(e)
				print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
	            		print "ERROR"
        	    		raise SystemExit

	#bus.add_signal_receiver(handler,
        #                        signal_name=None,
        #                        dbus_interface=None,
        #                        bus_name=None,
        #                        path=None)

	#dbus.Interface.connect_to_signal(None, handler)
	# property: print duration of file
	print "duration"+str(dbusIfaceProp.Duration())
	print "dbus Status:"+dbusIfaceProp.PlaybackStatus()



def pause():
        global dbusIfaceKey

        print "pause handler"

	# key: pause
	dbusIfaceKey.Action(dbus.Int32("16"))

def resume():
        global dbusIfaceKey

        print "resume handler"

	# key: un-pause after 5 seconds
	dbusIfaceKey.Action(dbus.Int32("16"))

def stop():
        global dbusIfaceKey, omxprocess

	try:
		dbusIfaceKey.Action(dbus.Int32("15"))
	except:
		print "stop command send failed"
	os.waitpid(omxprocess.pid, 0)


def get_omx_status():
	global dbusIfaceProp

	try:
		dbus_status = dbusIfaceProp.PlaybackStatus()
		return dbus_status
	except:
		return "stopped"


state="stopped"
socket_file="/tmp/rameplayer"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
        os.remove(socket_file)
except OSError:
        pass

s.bind(socket_file)


os.chmod(socket_file, 0o777)

while 1:

	s.listen(1)
	print "starting to listen " + socket_file

	conn, addr = s.accept()
	print "client connected"
	while 1:
        	data = conn.recv(1024)
        	if not data:
			break

		print data

		# update status
		omxstate=get_omx_status()
		if((state == "playing") & ("stopped" == omxstate)):
			stop()
                	state="stopped"
			display_lcd("Media stopped")

		# status
		if(data.find("ramecmd_status")==0):
			conn.send(state)

		# play
		if(data.find("ramecmd_play")==0):
			if(state == "playing"):
				pause()
                                state="paused"
                                display_lcd("Media paused")
			elif(state == "paused"):
                                resume()
                                state="playing"
                                display_lcd("Playing media")
			elif(state == "stopped"):
				play(data[13:])
				state="playing"
				display_lcd("Playing media")

		# pause
		if(data.find("ramecmd_pause")==0):
			if(state == "playing"):
                		pause()
				state="paused"
				display_lcd("Media paused")

		# resume
		if(data.find("ramecmd_resume")==0):
			if(state == "paused"):
                		resume()
				state="playing"
				display_lcd("Playing media")

		# stop
		if(data.find("ramecmd_stop")==0):
			if(state != "stopped"):
                		stop()
				state="stopped"
				display_lcd("Media stopped")

        	#conn.send(data)
        	print data

	conn.close()
