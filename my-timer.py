import threading
from datetime import datetime

main = threading.Thread(daemon=True)

def record():
    print(datetime.now())
    time = threading.Timer(interval=10, function=record)
    time.start()

main.start()
record()
main.join()
