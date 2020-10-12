#!/usr/bin/env python
import sys
import RPi.GPIO as GPIO

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

# read value
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
poweron = GPIO.input(21)
GPIO.cleanup(21)

def turnonheater():
    print "turn on heater"
    GPIO.setup(21,GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    GPIO.cleanup(21)
def turnoffheater():
    print "turnoffheater"
    GPIO.setup(21,GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    GPIO.cleanup(21)

turnoffheater()
#turnonheater()
