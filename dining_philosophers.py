'''
Philosophers sit around a table with a fork between each pair.
A philosopher needs both the left and right fork to eat.
Only one philosopher can hold a fork at a time.

Prevent deadlock: No philosopher should wait indefinitely.
Prevent starvation: Every philosopher should get a chance to eat.
'''

from typing import List
from threading import Lock, Thread
import time
import random

class Table:
  def __init__(self, num_philosophers):
    self.num_philosophers = num_philosophers
    self.num_forks = num_philosophers

    # allocate a lock per fork
    # lock[i] is the fork to the right of philosopher i
    self.locks: List[Lock] = []
    for _ in range(self.num_forks):
      new_lock = Lock()
      self.locks.append(new_lock)
  
  def eat(self, i):
    # ith philosopher is trying to eat
    right_fork_index = i
    left_fork_index = (i - 1) % self.num_philosophers

    right_fork = self.locks[right_fork_index]
    left_fork = self.locks[left_fork_index]

    # think
    time.sleep(random.uniform(1, 3))

    has_eaten = False
    while not has_eaten:

      # attempt to grab right fork
      right_fork.acquire()

      # think
      time.sleep(random.uniform(1, 3))
      
      # now i have the right fork
      # attempt to grab the left fork. timeout if needed.
      left_acquired = left_fork.acquire(timeout=2)

      # couldn't get fork. release other fork and try again
      if not left_acquired:
        print(f"{i}th diner could not get left fork. releasing right.")
        right_fork.release()
        time.sleep(1) # take a break before grabbing right fork again
        continue
        
      # got second fork! eat
      has_eaten = True
      print(f"{i}th diner has eaten!")
      left_fork.release()
      right_fork.release()

  def run(self):
    # thread per philosopher
    threads = []
    for i in range(self.num_philosophers):
      # new thread
      p = Thread(target=self.eat, args=(i,))
      threads.append(p)
      p.start()

table = Table(10)
table.run()

