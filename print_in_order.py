# goal: print things in order regardless of thread currently active
from threading import Thread, Lock

data = [1,2,3] # need to print in order
read_lock = Lock()

def reader(item_to_read):
  while True:
    # check if the first item is the one i need
    # first, acquire lock
    read_lock.acquire()
    # check first element
    if data[0] == item_to_read:
      data.pop(0)
      print(item_to_read)
      read_lock.release()
      break
    else:
      read_lock.release()



reader_thread_1 = Thread(target=reader, args=(1,))
reader_thread_2 = Thread(target=reader, args=(2,))
reader_thread_3 = Thread(target=reader, args=(3,))

reader_thread_3.start()
reader_thread_2.start()
reader_thread_1.start()

reader_thread_3.join()
reader_thread_2.join()
reader_thread_1.join()

# producer_thread = Thread(target=producer, args=(queue, range(10)))
# consumer_thread = Thread(target=consumer, args=(queue, 10))

# producer_thread.start()
# consumer_thread.start()

# producer_thread.join()
# consumer_thread.join()

print("All items have been processed.")