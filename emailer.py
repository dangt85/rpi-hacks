# IO libs
from gpiozero import MotionSensor, LightSensor, LED
from picamera import PiCamera

# email libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# std/misc libs
from os import environ
from datetime import datetime
from time import sleep

# init email settings
##from_address    = environ["EMAILER_FROM"]
##from_password   = environ["EMAILER_PASS"]
##to_addresses    = environ["EMAILER_TO"]

def send_email(current_time):
    filename = current_time + '.jpg'
        
    msg = MIMEMultipart()
    msg['Subject'] = 'Motion detected at the door at ' + current_time
    msg['From'] = from_address
    msg['To'] = to_addresses
    with open(filename, 'rb') as pic:
        pic = MIMEImage(pic.read())
    msg.attach(pic)
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(from_address, from_password)
    server.ehlo()
    server.send_message(msg, from_address, to_addresses)
    server.quit()

def go_active():
    current_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    print("Motion detected " + current_time)
    camera.capture(current_time + '.jpg')
    # send_email(current_time)
    camera.start_recording(current_time + '.h264')
    if not ldr.light_detected:
        print("turning light on!")
        light.on()

def go_inactive():    
    current_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    print("Motion ended " + current_time)
    camera.stop_recording()
    print("turning light off!")
    light.off()

prev_state = 0

camera = PiCamera()
pir = MotionSensor(17, queue_len = 1)
ldr = LightSensor(24, queue_len = 1)
light = LED(25)

try:
    print("Home watch start... (CTRL-C to exit)")
    print("Waiting for no motion...")

    pir.wait_for_no_motion()

    print("Ready!")

    light.off()

    # loop until user quits (CTRL+C)
    while True:

        if pir.motion_detected and prev_state == 0:
            go_active()
            prev_state = 1
        elif not pir.motion_detected:
            if prev_state == 1:
                go_inactive()
            prev_state = 0
        
        sleep(0.2)

except KeyboardInterrupt:
    print("Quitting...")
