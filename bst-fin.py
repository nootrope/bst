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
# gong = baseDir + 'gong.wav'	# utility notification
playThreshold = 10	# visitor goes in dress
playbackDuration = 20	# in seconds
slept = 0

def readSensor(s):
	try:
		inputAsInteger = int(s)
		if (inputAsInteger > 1023):
			#print '***** Tossing artifact ('+ str(inputAsInteger) + ')'
			pass
		else:
			# ***** DEBUG feedback:
			print inputAsInteger
			return inputAsInteger
	except ValueError:
		pass

sensorInput = serial.Serial(port, 9600)	# from Arduino
sensorInput.flushInput()

# def playtrack(track):
# 	slept = 0
# 	climax = pygame.mixer.Sound(track)
# 	channelA.play(climax)
# 	while channelA.get_busy():
# 		if (slept < playbackDuration):
# 			sleep(1)
# 			slept += 1
# 			if (slept > playbackDuration):
# 				channelA.pause()
# 				return playbackDuration
# 	return slept

try:
	pygame.mixer.init(48000, -16, 1, 1024)
	channelA = pygame.mixer.Channel(1)
except Exception, e:
	raise e

while True:
	if (readSensor(sensorInput.readline()) > playThreshold):
	 	for audioFile in tracks:
			climax = pygame.mixer.Sound(audioFile)
			channelA.play(climax)
	 		slept = playbackDuration - slept
			while channelA.get_busy():
				if (slept < playbackDuration):
					print "slept < 20 = " + str(slept)
					sleep(1)
					slept += 1
					print "slept = " + str(slept)
				else:
					channelA.pause()
					print "slept > 20 = " + str(slept)
					slept = 0
					print "slept reset = " + str(slept)
					sensorInput.flushInput()
					print "== sensorInput buffer flushed =="
					while (readSensor(sensorInput.readline()) < playThreshold):
						pass
					channelA.unpause()
