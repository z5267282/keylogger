#!/usr/bin/env python3

from AppKit import NSWorkspace
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    KEYS_LOG = 'keys.txt'
    MICE_LOG = 'mice.txt'
    APPS_LOG = 'apps.txt'

    def on_press(self, key):
        if (key == keyboard.Key.esc):
            self.done = True
            return False

        print(key)
    
    def on_click(self, x, y, button, pressed):
        if self.done:
            return False
        if pressed:
            print(button)

    def __init__(self):
        self.done = False
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)
    
    def run(self):
        self.keys.start()
        self.mice.start()

        app = get_focus_app_string()
        apps = dict()
        prev = None
        while not self.done:
            # Handle a newly seen app
            if prev is None or prev != app:
                print(f"{timestamp()} - '{app}'")

                if not app in apps:
                    apps[app] = 1
                else:
                    apps[app] += 1

                prev = app

            app = get_focus_app_string()                
        
        print('Most used apps in session:')
        for application, count in sort_dict_descending_keys(apps):
            print(f"'{application}' : {count}")

def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
