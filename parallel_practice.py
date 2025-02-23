from queue import Queue, Empty
from threading import Thread
import time

def producer(q):
    for i in range(10):
        item = f'item-{i}'
        q.put(item)
        print(f"Produced: {item}")
        time.sleep(1)
    print("producer done")

def consumer(q):
    while True:
        try: 
          item = q.get(block=True, timeout=3) # block. timeout of 3 seconds.
        except Empty:
            print('waited too long. stopping.')
            break
        if item is None:
            print("breaking")
            break
        print(f"Consumed: {item}")
        q.task_done()
    print("consumer done")

q = Queue()

consumer_thread = Thread(target=consumer, args=(q,))
producer_thread = Thread(target=producer, args=(q,))
producer_thread.start()
consumer_thread.start()
consumer_thread.join()
producer_thread.join()
q.put(None)  # Stop signal for consumer
# consumer_thread.join()
