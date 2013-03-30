#! /usr/bin/env python

import serial, sys, pygame.mixer
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

try:
	pygame.mixer.init(48000, -16, 1, 1024)
	channelA = pygame.mixer.Channel(1)
except Exception, e:
	raise e

def readSensor(s):
	try:
		inputAsInteger = int(s)
		if (inputAsInteger > 1023):
			#print '***** Tossing artifact ('+ str(inputAsInteger) + ')'
			pass
		else:
			# ***** DEBUG feedback:
			print "==> " + str(inputAsInteger)
			return inputAsInteger
	except ValueError:
		pass

sensorInput = serial.Serial(port, 9600)	# from Arduino
sensorInput.flushInput()

while True:
	if (readSensor(sensorInput.readline()) > playThreshold):
		print "Top if readSensor True!"
		sensorInput.flushInput()
		slept = 0
	 	for audioFile in tracks:
			climax = pygame.mixer.Sound(baseDir + audioFile)
			channelA.play(climax)
	 		print "Playing sample " + audioFile
	 		#slept = playbackDuration - slept
	 		#sensorInput.flushInput()
			while (channelA.get_busy() > 0):
				print "inWaiting(), slept, channelA.get_busy() = " + str(sensorInput.inWaiting()) + ", " + str(slept) + ", " + str(channelA.get_busy())
				if (slept < playbackDuration):
					#print "slept < 20 = " + str(slept)
					sleep(1)
					slept += 1
					print "slept = " + str(slept)
				else:
					channelA.pause()
					print "slept > 20 = " + str(slept)
					slept = 0
					print "slept reset, inWaiting to be flushed= " + str(slept) + ", " + str(sensorInput.inWaiting())
					sensorInput.flushInput()
					print "inWaiting(), " + str(sensorInput.inWaiting()) + "after sensorInput buffer flushed."
					print "readSensor = " + str(readSensor(sensorInput.readline())) + ". Stepping into while readSensor test."
					while (readSensor(sensorInput.readline()) < playThreshold):
						print "-"
						#pass
					print "+"
					channelA.unpause()
