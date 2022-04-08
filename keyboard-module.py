import keyboard

"""
    Playing around with: https://pypi.org/project/keyboard/
"""

def record_test():
    # Record events until 'esc' is pressed.
    recorded = keyboard.record(until='esc')

    keyboard.play(recorded)

def write_test():
    keyboard.write('Fishing in the river!\n', delay=0.1)

def strings_test():
    recorded = keyboard.record(until='esc')

    print(list(keyboard.get_typed_strings(recorded)))


if __name__ == '__main__':
    record_test()
    # write_test()
    # strings_test()