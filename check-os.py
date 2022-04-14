import os
import platform
import sys

# Testing from: https://stackoverflow.com/questions/8220108/how-do-i-check-the-operating-system-in-python

print(f"The operating system you're using is '{sys.platform}'")
print(f"The value of platform.system() is '{platform.system()}'")
print(f"The value of os.uname() is {os.uname()}")
