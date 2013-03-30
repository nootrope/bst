// Arduino code for Kathryn Cornelius's installation, Blood, Sweat, and Tears
// The Arduino will continuously send the smoothed analog value of analog pin 0
//   can include a period of calibration for debugging with SparkFun's DangerShield

// Uses smoothing code from:
// http://www.arduino.cc/en/Tutorial/Smoothing
// created 22 April 2007
// By David A. Mellis  <dam@mellis.org>
// modified 9 Apr 2012 by Tom Igoe
// and
// calibration code from:
// http://arduino.cc/en/Tutorial/Calibration
// created 29 Oct 2008
// By David A Mellis
// modified 30 Aug 2011 by Tom Igoe
//
// Both:
// modified 20 March 2013 by Alberto Gaitán

// ********** Globals *****
const int inputPin = A0;	// piezo input
const int ledPin = 13;	// utility LED
int state = B00000001;	// to toggle ledPin state
// for smoothing
const int numReadings = 10;
int readings[numReadings];	// the readings from the analog input
int index = 0;	// the index of the current reading
int total = 0;	// the running total
int average = 0;	// the average

// for calibration
//int sensorValue = 0;
//int sensorMin = 1023;	// to be recalculated for minimum sensor value
//int sensorMax = 0;	// to be recalculated for maximum sensor value
//byte clipped = 0;	// initialize sensor-constrained flag

// for normal operation
int sensorMin = 0;
int sensorMax = 1023;

// ********** DEBUG and test w/DangerShield ******
const int LED1 = 5;
const int LED2 = 6;

void setup() {
	pinMode(ledPin, OUTPUT);

	digitalWrite(ledPin, (state ^ 0));

	// DEBUG and test with DangerShield
	pinMode(LED1, OUTPUT);
	pinMode(LED2, OUTPUT);

	// zero out smoothing array
	for (int thisReading = 0; thisReading < numReadings; thisReading++) readings[thisReading] = 0;

	Serial.begin(9600);

	// ******* Calibrate the input *****
	// indicate(ledPin);
	// digitalWrite(ledPin, HIGH);	// begin calibration
	// digitalWrite(LED1, HIGH);      // DEBUG w/DangerShield
	// while (millis() < 10000) {
	// 	sensorValue = analogRead(inputPin);
	// 	// record the maximum sensor value
	// 	if (sensorValue > sensorMax) {
	// 		sensorMax = sensorValue;
	// 	}
	// 	// record the minimum sensor value
	// 	if (sensorValue < sensorMin) {
	// 		sensorMin = sensorValue;
	// 	}
	// }
	// digitalWrite(ledPin, LOW);	// end calibration		
	// digitalWrite(LED1, LOW);      // DEBUG w/DangerShield
	// indicate(ledPin);
	// ******* End calibration *******
}

// void indicate(int led) {
// 	for (int i = 0; i < 6; i++) {
// 		digitalWrite(led, HIGH);
// 		delay(200);
// 		digitalWrite(led, LOW);
// 		delay(150);
// 	}
// 	delay(500);
// }

void loop() {

	// ******* Determine smoothed value *****
	// subtract the last reading:
	total= total - readings[index];
	// read from the sensor:
	readings[index] = analogRead(inputPin);
	// add the reading to the total:
	total= total + readings[index];
	// advance to the next position in the array:
	index = index + 1;
	// if we're at the end of the array...
	if (index >= numReadings)
		// ...wrap around to the beginning:
		index = 0;
	// calculate the average:
	average = total / numReadings;

	// apply the calibration, if any, to the sensor reading
	average = map(average, sensorMin, sensorMax, 0, 1023);
	
	// in case the sensor value is outside the range seen during calibration
  average = constrain(average, 0, 1023);
  //digitalWrite(LED2, HIGH);

	// send (calibrated and) smoothed sensor value to the RasPi as ASCII digits
	digitalWrite(ledPin, (state ^ 0));
	Serial.println(average, DEC);
	delay(250);        // delay in between reads for stability
}
