import threading
from datetime import datetime

main = threading.Thread(daemon=True)

def record():
    print(datetime.now())
    time = threading.Timer(interval=1, function=record)
    time.start()

main.start()
record()
main.join()
