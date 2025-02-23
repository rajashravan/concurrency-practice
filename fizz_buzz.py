# distributed/multi threaded fizz buzz
from threading import Lock, Thread

class ConcurrentFizzBuzz:
  def __init__(self, n):
    self.lock = Lock() # for editting cur
    self.cur = 1
    self.n = n

  def is_div_by_3(self):
    return (self.cur % 3) == 0
  
  def is_div_by_5(self):
    return (self.cur % 5) == 0
  
  def fizz(self):
    while True:
      with self.lock:
        if self.cur > self.n:
          break
        if self.is_div_by_3() and not self.is_div_by_5():
          print("Fizz")
          self.cur += 1
  
  def buzz(self):
    while True:
      with self.lock:
        if self.cur > self.n:
          break
        if not self.is_div_by_3() and self.is_div_by_5():
          print("Buzz")
          self.cur += 1

  def fizzbuzz(self):
    while True:
      with self.lock:
        if self.cur > self.n:
          break
        if self.is_div_by_3() and self.is_div_by_5():
          print("FizzBuzz")
          self.cur += 1

  def regular(self):
    while True:
      with self.lock:
        if self.cur > self.n:
          break
        if not self.is_div_by_3() and not self.is_div_by_5():
          print(self.cur)
          self.cur += 1

  def run(self):
    # spin up 4 threads
    thread_fizz = Thread(target=self.fizz)
    thread_buzz = Thread(target=self.buzz)
    thread_fizzbuzz = Thread(target=self.fizzbuzz)
    thread_regular = Thread(target=self.regular)

    thread_fizz.start()
    thread_buzz.start()
    thread_fizzbuzz.start()
    thread_regular.start()

    # wait
    thread_fizz.join()
    thread_buzz.join()
    thread_fizzbuzz.join()
    thread_regular.join()

main = ConcurrentFizzBuzz(50)
main.run()