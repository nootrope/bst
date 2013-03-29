#! /usr/bin/env python

import serial, sys, subprocess, pygame.mixer
from time import sleep

# Usage example: python bst.py /dev/ttyUSB0
if (len(sys.argv) != 2):
	print("Usage: python bst.py [tty-port]")
	sys.exit()
port = sys.argv[1]

baseDir = '/home/alberto/cornelius/audio/'
tracks = ['20121209-205217-edited.wav', '20121210-103310-edited.wav', '20121216-142614-edited.wav', '20121219-145044-edited.wav', '20121220-150925-edited.wav']
gong = baseDir + 'gong.wav'	# utility notification
playThreshold = 10	# visitor goes in dress
takeABreath = 3	# in seconds

sensorInput = serial.Serial(port, 9600)	# from Arduino
sensorInput.flushInput()

def readSensor(s):
	try:
		inputAsInteger = int(s)
		if (inputAsInteger > 1023):
			print '***** Tossing artifact ('+ str(inputAsInteger) + ')'
			pass
		else:
	#		***** DEBUG feedback:
			print inputAsInteger
			return inputAsInteger
	except ValueError:
		pass

def playtrack(track):
	climax = pygame.mixer.Sound(track)
	sleep(takeABreath)
	channelA.play(climax)
	while channelA.get_busy():
#		if readSensor(sensorInput.readline()) < playThreshold:
#			channelA.fadeout(1000)
#			channelA.pause()
#			channelA.stop()
#			print '***** below playThreshold'
#			return False
#		sleep(0.1)
		pass
	return True

try:
	pygame.mixer.init(48000, -16, 1, 1024)
	channelA = pygame.mixer.Channel(1)
except Exception, e:
	raise e

while True:
	if (readSensor(sensorInput.readline()) > playThreshold):
	 	for bigOh in tracks:
	 		if not playtrack(baseDir + bigOh):
	 			#sensorInput.flushInput()
 				break	# quit-threshold has been met
