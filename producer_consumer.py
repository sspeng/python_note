#! /usr/bin/python3 
# -*- coding: utf-8

import time
import queue
import random
import threading

is_producing = True
prod_lock = threading.Lock()

is_moving = True
move_lock = threading.Lock()

MAXSIZE = 100


class Producer(threading.Thread):
    def __init__(self, thread_name: str, prod_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.prod_buffer = prod_buffer

    def run(self):
        global is_producing
        global prod_lock
        for i in range(MAXSIZE):
            item = random.randint(0, 1000)
            print('%s : %s is producing %d to the producer buffer' % (time.ctime(), self.getName(), item))
            self.prod_buffer.put(item)
            time.sleep(random.random())
        print('%s : %s finished!' % (time.ctime(), self.getName()))
        prod_lock.acquire()
        is_producing = False
        prod_lock.release()


class Mover(threading.Thread):
    def __init__(self, thread_name: str, prod_buffer: queue.Queue, mov_buffer: queue.Queue, con_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.prod_buffer = prod_buffer
        self.mov_buffer = mov_buffer
        self.con_buffer = con_buffer

    def run(self):
        global is_producing
        global is_moving
        global prod_lock
        global move_lock
        while not self.prod_buffer.empty() or is_producing:
            item = self.prod_buffer.get()
            time.sleep(random.random())
            print('%s : %s is moving %d to the Mover buffer' % (time.ctime(), self.getName(), item))
            self.mov_buffer.put(item)
            time.sleep(random.random())
            item = self.mov_buffer.get()
            print('%s : %s is moving %d to the Consumer buffer' % (time.ctime(), self.getName(), item))
            self.con_buffer.put(item)
            prod_lock.acquire()
            if not is_producing and self.prod_buffer.empty():
                prod_lock.release()
                break
            prod_lock.release()
        move_lock.acquire()
        is_moving = False
        move_lock.release()


class Consumer(threading.Thread):
    def __init__(self, thread_name: str, con_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.con_buffer = con_buffer
        self.count = 0
        self.sum = 0

    def run(self):
        global is_moving
        global move_lock
        while not self.con_buffer.empty() or is_moving:
            item = self.con_buffer.get()
            print('%s : %s is consuming, %d in the queue is consumed!' % (time.ctime(), self.getName(), item))
            self.sum += item
            self.con_buffer.task_done()
            self.count = self.count + 1
            move_lock.acquire()
            if not is_moving and self.con_buffer.empty():
                move_lock.release()
                break
            move_lock.release()
        print('%s : %s consumer finish, %d items is consumed, sum is %d'
              % (time.ctime(), self.getName(), self.count, self.sum))


def main():
    producer_buffer = queue.Queue(maxsize=MAXSIZE)
    mover_buffer = queue.Queue(maxsize=MAXSIZE)
    consumer_buffer = queue.Queue(maxsize=MAXSIZE)
    producer = Producer('producer', prod_buffer=producer_buffer)
    mover = Mover('Mover', prod_buffer=producer_buffer, mov_buffer=mover_buffer, con_buffer=consumer_buffer)
    consumer = Consumer('consumer', con_buffer=consumer_buffer)
    producer.start()
    mover.start()
    consumer.start()
    producer.join()
    mover.join()
    consumer.join()
    print('all thread finish')


if __name__ == '__main__':
    main()
