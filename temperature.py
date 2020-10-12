#!/usr/bin/env python

import MySQLdb
from MySQLdb import Error
import urllib2
import json
import RPi.GPIO as GPIO


# read value
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
poweron = GPIO.input(21)
GPIO.cleanup(21)

def turnonheater():
    print "turn on heater"
    GPIO.setup(21,GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
#    GPIO.cleanup(21)

def turnoffheater():
    print "turnoffheater"
    GPIO.setup(21,GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
#    GPIO.cleanup(21)
# check online how to find your w1/device folder
# maybe here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20
tfile = open("/sys/bus/w1/devices/28-000005889a93/w1_slave")
text = tfile.read()
tfile.close()
temperature_data = text.split()[-1]
temperature = float(temperature_data[2:])
temperature = temperature / 1000
print temperature

db = MySQLdb.connect(MYSQLSECRETS)
curs = db.cursor()

try:
    print "database call"
    curs.execute ("SELECT * FROM thermostaat")
    row = curs.fetchone()
    onoff = row[1]
    #print "onoff:"+str(onoff)
    thermostemp = row[2]
    print "temp thres " + str(row[2])
    if onoff == 1 and row[2] > temperature:
        print "temp is lower than threshold"
        turnonheater()
    elif onoff == 1 and row[2] < temperature:
        print "temp is higher"
        turnoffheater()
    elif onoff == 0:
        print "turn off"
        turnoffheater()

except Error as e:
    print (e)


try:
    print "query db..."
    q = "INSERT INTO temperatures(temperature) VALUES("+str(temperature)+");"
    print  q
    curs.execute(q)
    db.commit()
    print "Data committed"

except:
    print "Error: the database is being rolled back"
    db.rollback()


finally:
    curs.close()
    db.close()
