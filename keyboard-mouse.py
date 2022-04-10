from pynput import keyboard, mouse

# Testing to see keyboard inputs and mouse clicks

done = False

def on_press(key):
    try:
        print(key.char, end='')
    except AttributeError:
        print(key, end='')

def on_release(key):
    # Just escape for now
    if key == keyboard.Key.esc:
        done = True
        return False

def on_click(x, y, button, pressed):
    print(f'({x},{y}), {button}, {pressed}')

k = keyboard.Listener(on_press=on_press, on_release=on_release)
k.start()
k.join()

m = mouse.Listener(on_click=on_click)
m.start()
m.join()
if done:
    m.stop()
