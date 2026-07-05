# condition variable version

import threading
import time
import random

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item):
        with self.not_full:
            while len(self.queue) == self.capacity:
                self.not_full.wait()      # release lock and go to sleep atomically
            self.queue.append(item)
            self.not_empty.notify()       # wake up a waiting get()

    def get(self):
        with self.not_empty:
            while len(self.queue) == 0:
                self.not_empty.wait()     # release lock and go to sleep atomically
            item = self.queue.pop(0)
            self.not_full.notify()        # wake up a waiting put()
            return item


# --- Test harness ---
def producer(bq, n, name):
    for i in range(n):
        item = f"{name}-{i}"
        bq.put(item)
        print(f"[PUT] {item}")
        time.sleep(random.uniform(0, 0.05))

def consumer(bq, n, name):
    for _ in range(n):
        item = bq.get()
        print(f"[GET] {item} (by {name})")
        time.sleep(random.uniform(0, 0.1))

if __name__ == "__main__":
    bq = BoundedBlockingQueue(capacity=3)
    threads = [
        threading.Thread(target=producer, args=(bq, 10, "P1")),
        threading.Thread(target=producer, args=(bq, 10, "P2")),
        threading.Thread(target=consumer, args=(bq, 10, "C1")),
        threading.Thread(target=consumer, args=(bq, 10, "C2")),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Done — queue should be empty:", len(bq.queue) == 0)