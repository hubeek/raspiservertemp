#!/usr/bin/env python
import json
import urllib2
import MySQLdb

data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Amsterdam&units=metric&appid=CREATE_YOUR_WEATHER_API_ID'))

temperature = data["main"]["temp"]

db = MySQLdb.connect(MYSQLSECRETS)
curs = db.cursor()


try:
    print "query db..."
    q = "INSERT INTO weatherapi(temperature) VALUES("+str(temperature)+");"
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
