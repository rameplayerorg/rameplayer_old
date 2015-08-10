#!/usr/bin/python
#
# Copyright 2015 rameplayerorg
# Licensed under GPLv2, which you must read from the included LICENSE file.
#
# Handle's local device buttons and call's omx_server and lcd_server
#

from time import sleep
import RPi.GPIO as GPIO
import os
import socket
import time
from threading import Thread
import commands
import socket, time


def display_lcd(cmd):
        print "display_lcd:" + cmd
        try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect("/tmp/lcd_server")
                s.send("display " + cmd)
                s.close()
        except:
                print "display_lcd failed"



def get_omx_status():
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/rameplayer")
        s.send('ramecmd_status')
	data = s.recv(1024)
	print "ramecmd_status:" + data
        s.close()
	return data


def send_omx_cmd(cmd):
        print cmd
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/rameplayer")
        s.send(cmd)
        if(cmd=='ramecmd_status'):
                data = s.recv(1024)
                print "ramecmd_status:" + data
        s.close()




# get local IP Address
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
	local_ip_address = s.getsockname()[0]
except:
	local_ip_address = "NO NETWORK"

print local_ip_address


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP) # play
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # stop
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Up
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) # down


numcolumns = 16
numrows = 2
files = []
selected_index=0
mediadir="/media/data/"
state = 0 # 0=stopped, 1=playing, 2=paused
mediatype=""
busy=0



#os.system("mkfifo /tmp/cmd")
#os.system("/home/pi/lcdi2c -i -b 1")


# Get devicename from configfile
devicename=commands.getoutput("/usr/bin/cfget -C /media/config/config.ini mediaplayer/devicename")
print devicename

def show_lcd_message(row1, row2):
	print len(row1)

	row1=row1+"                 "
	row2=row2+"                 "

	display_lcd(row1[0:16] + row2[0:16])


show_lcd_message(str(devicename), local_ip_address)
print "devicename:"+devicename
print "devicename:"

def button_play_pressed(channel):
	global mediatype,mediadir, files, selected_index, state, busy
	file = mediadir+files[selected_index]
	print("Play pressed")

	if(0==state):
		print("Playing")
		state=1
		if(file.endswith(".mp3")):
			mediatype="video"
			show_lcd_message("Playing audio","")
			busy=0
			os.system("/home/pi/play_video.sh "+file)
			print("Ended")
			busy=1

			if(0!=state):
				state=0
				if(len(files)>(selected_index+1)):
                        		selected_index = selected_index + 1
			show_selected("play ended")

		elif(file.endswith(".mp4")):
			mediatype="video"
			show_lcd_message("Playing media","")
			busy=0
			os.system("/home/pi/play_video.sh "+file)
			print("Ended")
			busy = 1
			if(0!=state):
				state=0
				if(len(files)>(selected_index+1)):
                        		selected_index = selected_index + 1
			show_selected("play ended")
		else:
			mediatype="image"
			show_lcd_message("Playing media", "")
			os.system("/home/pi/show_image.sh "+file)
			print "displaying image"

			if(len(files)>(selected_index+1)):
				selected_index = selected_index + 1



	elif(1==state):
		if(mediatype=="image"):
			print "mediatype:image"
			return

		# playing
                show_lcd_message("Paused", "")
		os.system("/home/pi/pause_video.sh")
		state = 2

	elif(2==state):
                # paused
                os.system("/home/pi/resume_video.sh")
                state = 1
                show_lcd_message("Playing media", "")

	#show_selected()
	busy=0


def button_stop_pressed(channel):
	global mediatype,files, selected_index,state, busy
	state = 0
        print("Stop pressed")
	if(mediatype=="video"):
		print "stop-video"
		os.system("/home/pi/stop_video.sh")
	if(mediatype=="image"):
		print "show-background"
		os.system("/home/pi/show_background.sh")

	#if(len(files)>(selected_index+1)):
        #	selected_index = selected_index + 1

	#show_selected("stop")
	#busy=0


def  button_up_pressed(channel):
	global files, selected_index, state, busy

	if(0==state):
        	print("Up pressed!")
		print len(files)
		if(len(files)>(selected_index+1)):
			selected_index = selected_index + 1
		show_selected("up")
	busy=0


def  button_down_pressed(channel):
	global files, selected_index, state, busy

	if(0==state):
        	print("Down pressed!")
		if(selected_index>0):
                	selected_index = selected_index - 1
        	show_selected("down")
	busy=0


def show_selected(caller):
	print "show_selected:" + files[selected_index]+":"+caller
	show_lcd_message(files[selected_index], files[selected_index][16:])
	#print "lcd disabled"


def button_up_pressed_main(channel):
        global busy
	print "up key handler"
	if(0==busy):
		busy=1
        	t = Thread(target=button_up_pressed, args=(1,))
        	t.start()

def button_down_pressed_main(channel):
	global busy
        print "down key handler"
	if(0==busy):
                busy=1
        	t = Thread(target=button_down_pressed, args=(1,))
        	t.start()

def button_play_pressed_main(channel):
	global busy, mediadir, files, selected_index
        file = mediadir+files[selected_index]

	print "play handler"
	send_omx_cmd('ramecmd_play '+file)
	#if(0==busy):
        #        busy=1
	#	t = Thread(target=button_play_pressed, args=(1,))
	#	t.start()


def button_stop_pressed_main(channel):
	global busy
        print "stop handler"
	send_omx_cmd('ramecmd_stop')

       	#t = Thread(target=button_stop_pressed, args=(1,))
        #t.start()


GPIO.add_event_detect(7, GPIO.FALLING, callback=button_play_pressed_main, bouncetime=300)
GPIO.add_event_detect(11, GPIO.FALLING, callback=button_stop_pressed_main, bouncetime=300)
GPIO.add_event_detect(13, GPIO.FALLING, callback=button_up_pressed_main, bouncetime=300)
GPIO.add_event_detect(15, GPIO.FALLING, callback=button_down_pressed_main, bouncetime=300)


for file in os.listdir("/media/data"):
	if file.endswith(".mp4"):
		files.append(file)
		#print file
	if file.endswith(".mp3"):
                files.append(file)
                #print file
	#if file.endswith(".jpg"):
	#	if(file != "background.jpg"):
	#		files.append(file)
        #        #print file
	#if file.endswith(".png"):
	#	files.append(file)
        #        #print file
files.sort()
for file in files:
	print file

print "----------"
print files[1]


#time.sleep(10)
#show_selected()

i=0
while True:
	i=0
	time.sleep(0.5)
	get_omx_status()
