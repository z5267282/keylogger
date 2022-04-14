from AppKit import NSWorkspace

# Testing from https://stackoverflow.com/questions/3324372/finding-the-app-window-currently-in-focus-on-mac-osx

workspace = NSWorkspace.sharedWorkspace()
active_app = workspace.activeApplication()['NSApplicationName']
print(active_app)

prev = active_app
while True:
    active_app = workspace.activeApplication()['NSApplicationName']   
    if prev != active_app:
        print(active_app)
        prev = active_app
