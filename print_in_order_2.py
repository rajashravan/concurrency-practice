from threading import Lock, Thread

# goal: print 1,2,3 in order
# use locks to control the order

# the "gate" between 1 and 2, and then 2-3
lock_1_2 = Lock()
lock_2_3 = Lock()

# they start locked
lock_1_2.acquire()
lock_2_3.acquire()

def first():
  # no locks needed to acquire, since nothing
  # is blocking 1
  print("first")
  
  # open lock to second
  lock_1_2.release()

def second():
  # wait to acquire lock_1_2
  lock_1_2.acquire(blocking=True)
  print("second")
  lock_2_3.release()

def third():
  lock_2_3.acquire(blocking=True)
  print("third")

# spin up threads, any order
Thread(target=second).start()
Thread(target=third).start()
Thread(target=first).start()

# no need to wait
