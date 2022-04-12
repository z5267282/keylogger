from pynput import keyboard, mouse

# Testing to see keyboard inputs and mouse clicks

done = False

keys = str()
mice = list()

def on_press(key):
    global keys
    try:
        keys += key.char
    except AttributeError:
        if key == keyboard.Key.esc:
            global done
            done = True
            return False

def on_click(x, y, button, pressed):
    if pressed:
        mice.append(f'({x},{y}), {button}, {pressed}')

k = keyboard.Listener(on_press=on_press)
k.start()

m = mouse.Listener(on_click=on_click)
m.start()

while not done:
    pass

m.stop()

print('Keys:')
print(keys)

print('\nMice')
print('\n'.join(mice))
