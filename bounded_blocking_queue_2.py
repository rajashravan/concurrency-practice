# condition variable version

import threading
import time
import random

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = []

        # we need a lock to manage the queu
        self.lock = threading.Lock()

        # we use 2 condition variables
        # naming convention:
        # name the variable after the condition that you WANT to be true
        # in order for waiting threads to be woken up.
        self.has_space = threading.Condition(self.lock) # for put calls. we name it has_space because put calls need space to be avail for them to proceed
        self.has_items = threading.Condition(self.lock)

    def put(self, item):
        with self.has_space:
            while len(self.queue) == self.capacity:
                # queue is full, so we need to wait and sleep in one atomic action
                self.has_space.wait() # wait for this to no longer be true
            
            # if queue is not full, we can place on to it, and tell people stuff is there
            self.queue.append(item)
            self.has_items.notify()

    def get(self):
        # in order to get/read from the queue, we use the has_items cond variable
        with self.has_items:
            while len(self.queue) == 0:
                # this condition is not true, so we release and wait on the lock
                self.has_items.wait()
            
            # if the above IF never triggered, then we know that
            # we have elements in the queue to read from
            item_to_return = self.queue.pop(0) # get the element
            self.has_space.notify() # the queue has space now, tell threads waiting on it
            return item_to_return


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