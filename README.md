# bst
## Code for Kathryn Cornelius's installation: Blood, Sweat, and Tears
### Curator's Office, 1515 14th St, NW, Washington, DC
#### March 30, 2013 - May 10, 2013

An Arduino continuously sends the smoothed analog value of a vibation sensor attached to the hanging system for the dress that is the centerpiece of the exhibition. The analog signal is sent via Serial.println() to a Raspberry Pi (B) running Raspbian Linux version 3.6.11+ (dc4@dc4-arm-01) (gcc version 4.7.2 20120731 (prerelease) (crosstool-NG linaro-1.13.1+bzr2458 - Linaro GCC 2012.08)) and Python 2.7

A python script, ~/bst-fin.py provides the interactivity and plays the installation's audio.

_Requires [pygame](http://www.pygame.org/news.html) and [pySerial](http://pyserial.sourceforge.net/pyserial.html)_

The Arduino code uses [smoothing code](http://www.arduino.cc/en/Tutorial/Smoothing) created 22 April 2007 By David A. Mellis and modified 9 Apr 2012 by Tom Igoe, and [calibration code](http://arduino.cc/en/Tutorial/Calibration) created 29 Oct 2008 by David A Mellis and modified 30 Aug 2011 by Tom Igoe; both modified 20 March 2013 by Alberto Gaitán

