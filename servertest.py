#!/usr/bin/env python
import smtplib
import httplib
import datetime
import time
import shutil
import MySQLdb
from MySQLdb import Error


GMAILSECRETS
start = time.clock()
site1 = "xofoon"
site2 = "www.snipperlog"
site3 = "app-all"
site4 = "hjh.devsnips"
site5 = "brechtjezwaneveld"
site6 = "escherensemble"


db = MySQLdb.connect(MYSQLSECRETS)
curs = db.cursor()

def send_email(recipient, subject, text):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + recipient + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + subject + '\n'
    msg = header + '\n' + text + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, recipient, msg)
    smtpserver.close()

def get_status_code(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        conn = httplib.HTTPSConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None

def grabFor(site):
    statuscode = str(get_status_code(site+".nl"))
    timetaken = time.clock() - start
    timetakenstr = str(timetaken)
    print("status " + statuscode)
    print ("time " + timetakenstr)
    values = "'" +  site + "', " + timetakenstr + ", " + statuscode
    print("valuestring "+ values)
    query = "INSERT INTO serverresponses(serverurl,responsetime, statuscode) VALUES(" + values + ");"
    print("query "+ query)
    try:
        print( "statuscode " + statuscode)
        curs.execute(query)
        db.commit()
        print ("Data committed")
    except Error as e:
        print ("Error: the database is being rolled back" + e)
        db.rollback()

    if  get_status_code(site+".nl") != 200 or get_status_code(site+".nl" != 302) :
        #f = open("/var/www/html/files/logfile."+site+".txt", "a")
        #f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' CONNECTION ERROR '+statuscode + '\n' )
        #f.close()
        print ("CRON ERROR")
        send_email('hjhubeek@gmail.com', site + ' server not at 200', site + ' server at '+statuscode)

    else:
        timetaken = time.clock() - start
        #f = open("/var/www/html/files/logfile."+site+".txt", "a")
        #f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' status == 200 ' + str(timetaken) + '\n' )
#        f.close()
        print (" 200" + str(timetaken))


grabFor(site1)
start = time.clock()
grabFor(site2)
start = time.clock()
grabFor(site3)
start = time.clock()
grabFor(site4)
start = time.clock()
grabFor(site5)
start = time.clock()
grabFor(site6)
