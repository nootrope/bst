import serial, sys

# Usage example: python ReadSerial.py /dev/ttyUSB0

if (len(sys.argv) != 2):
	print("Usage: python ReadSerial.py port")
	sys.exit()
port = sys.argv[1]

serialFromArduino = serial.Serial(port,9600)
serialFromArduino.flushInput()
while True:
	input = serialFromArduino.readline()
	try:
 		inputAsInteger = int(input)
		print (inputAsInteger)
	except ValueError:
		pass

