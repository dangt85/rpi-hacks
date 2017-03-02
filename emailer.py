#!/usr/bin/env python

# sensor lib
import RPi.GPIO as GPIO

# email libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# cam libs
from picamera import PiCamera

# std/misc libs
import os
import datetime
import time

# init motion sensor settings
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 4

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN) # Echo

curr_state = 0
prev_state = 0

# init email settings
from_address = os.environ["EMAILER_FROM"]
from_password = os.environ["EMAILER_PASS"]
to_addresses = os.environ["EMAILER_TO"]

def take_picture():
    current_time = str(datetime.datetime.now())
    current_time = current_time[0:19]
    with PiCamera() as camera:
        camera.resolution = (800, 600)
        camera.framerate = 24
        camera.capture((current_time)+'.jpg')
        return ((current_time)+'.jpg')

def email_send(file):
    current_time = str(datetime.datetime.now())
    current_time = current_time[0:19]
        
    msg = MIMEMultipart()
    msg['Subject'] = 'Motion detected at the door at '+current_time
    msg['From'] = from_address
    msg['To'] = to_addresses
    with open(file, 'rb') as pic:
        pic = MIMEImage(pic.read())
    msg.attach(pic)
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(from_address, from_password)
    server.ehlo()
    server.send_message(msg, from_address, to_addresses)
    server.quit()

print("Home watch start... (CTRL-C to exit)")
print("Waiting for PIR to settle...")

try:
    # loop until PIR is 0 ("ready state")
    while GPIO.input(GPIO_PIR) == 1:
        curr_state = 0

    print("   Ready...")

    # loop until user quits (CTRL+C)
    while True:
        # read PIR state
        curr_state = GPIO.input(GPIO_PIR)

        if curr_state == 1 and prev_state == 0:
            print("   Motion detected!")
            file = take_picture()
            email_send(file)

            # record previous state
            prev_state = 1
        elif curr_state == 0 and prev_state == 1:
            # PIR has returned to ready state
            print("   Ready...")
            prev_state = 0

        # wait 10 milisecs
        time.sleep(0.01)

except KeyboardInterrupt:
    print("   Quit")
    # reset GPIO settings
    GPIO.cleanup()
