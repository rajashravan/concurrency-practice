from threading import Thread, Lock
import time

read_lock = Lock()
write_lock = Lock()
data = []

def reader():
    while True:
        read_lock.acquire()
        print(f"Reading Data: {data}")
        read_lock.release()
        time.sleep(1)

def writer():
    global data
    while True:
        write_lock.acquire()
        # read_lock.acquire()
        data.append("new data")
        print("Data Written.")
        # read_lock.release()
        write_lock.release()
        time.sleep(2)

Thread(target=reader).start()
Thread(target=writer).start()
