# Tuinhok

## Servertest

checks if servers my are online

## Temperaturetest
- measures the temp on rasp
- validates with thermostaat in db => turns on off heater

## cronjobs
sudo crontab -e
5 * * * * python /home/pi/raspiservertest/servertest.py 

5 * * * * python /home/pi/raspiservertest/temperature.py 

5 * * * * python /home/pi/raspiservertest/weatherapi.py 


todo:
cleanup in cron.
