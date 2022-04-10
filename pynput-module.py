from pynput import keyboard

def on_press(key):
    try:
        print(key.char, end='')
    except AttributeError:
        print(key, end='')

def on_release(key):
    if key == keyboard.Key.esc:
        # In the callback this is how we stop the listener
        return False

def with_statement():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release
    ) as listener:
        listener.join()

def no_with():
    # the non-blocking approach: we want to track other inputs later
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    listener.join()
    # try:
    #     listener.wait()
    #     listener.join()
    # finally:
    #     listener.stop()

# with_statement()
no_with()
