import keyboard

"""
    Playing around with: https://pypi.org/project/keyboard/
"""

# Record events until 'esc' is pressed.
recorded = keyboard.record(until='esc')
# Then replay back at three times the speed.
keyboard.play(recorded, speed_factor=3)
