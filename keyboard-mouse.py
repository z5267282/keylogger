from pynput import keyboard, mouse

def on_press(key):
    try:
        print(key.char, end='')
    except AttributeError:
        print(key, end='')

def on_click(x, y, button, pressed):
    print(f'({x},{y}), {button}, {pressed}')

with keyboard.Listener(on_press=on_press) as k:
    k.join()

with mouse.Listener(on_click=on_click) as m:
    m.join()
