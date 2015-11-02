from mail_settings import *
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from picamera import PiCamera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


print(email,password)
global file
PIR = 17
GPIO.setup(PIR, GPIO.IN)

def takepic():
    global file
    current_time = str(datetime.datetime.now())
    current_time = current_time[0:19]
    with PiCamera() as camera:
        camera.resolution = (800, 600)
        camera.framerate = 24
        camera.capture((current_time)+'.jpg')
        takepic.file = ((current_time)+'.jpg')
        

def email_send(to,file):
    current_time = str(datetime.datetime.now())
    current_time = current_time[0:19]
    msg = MIMEMultipart()
    msg['Subject'] = 'ALERT - AT '+current_time+' THE POST HAS ARRIVED'
    msg['From'] = email
    msg['To'] = to
    with open(takepic.file, 'rb') as pic:
        pic = MIMEImage(pic.read())
    msg.attach(pic)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    server.ehlo()
    server.send_message(msg)
    server.quit()

while True:
    time.sleep(1)
    if GPIO.input(PIR) == 1:
        takepic()
        email_send(email,takepic.file)
        time.sleep(1)
    else:
        print("Waiting for postie")
        time.sleep(0.1)
