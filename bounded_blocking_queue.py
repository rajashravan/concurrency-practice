import time
from threading import Thread, Lock, Semaphore

class BoundedBlockingQueue:
    def __init__(self, max_size):
        self.data = []
        self.max_size = max_size
        self.lock = Lock()

        # Semaphores for controlling queue capacity
        self.empty_slots = Semaphore(max_size)  # Start with max empty slots
        self.available_items = Semaphore(0)     # Start with 0 items

    def enqueue(self, item):
        self.empty_slots.acquire()  # Wait if no empty slots
        with self.lock:
            self.data.append(item)
            print(f"Enqueued: {item}")
        self.available_items.release()  # Signal that a new item is available

    def dequeue(self):
        self.available_items.acquire()  # Wait if no available items
        with self.lock:
            item = self.data.pop(0)
            print(f"Dequeued: {item}")
        self.empty_slots.release()  # Signal that a slot is now empty
        return item

# Testing the BoundedBlockingQueue with Multiple Producers and Consumers
def producer(queue, items):
    for item in items:
        queue.enqueue(item)
        time.sleep(0.5)  # Simulate time to produce an item

def consumer(queue, num_items):
    for _ in range(num_items):
        item = queue.dequeue()
        time.sleep(1)  # Simulate time to consume an item

queue = BoundedBlockingQueue(max_size=5)

# Start producer and consumer threads
producer_thread = Thread(target=producer, args=(queue, range(10)))
consumer_thread = Thread(target=consumer, args=(queue, 10))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("All items have been processed.")
