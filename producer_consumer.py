#! /usr/bin/python3 
# -*- coding: utf-8

import time
import queue
import random
import threading

is_continue = True

MAXSIZE = 100


class Producer(threading.Thread):
    def __init__(self, thread_name: str, prod_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.prod_buffer = prod_buffer

    def run(self):
        global is_continue
        for i in range(MAXSIZE):
            print('%s : %s is producing %d to the producer buffer' % (time.ctime(), self.getName(), i))
            self.prod_buffer.put(random.randint(1, 1000))
            time.sleep(random.random())
        print('%s : %s finished!' % (time.ctime(), self.getName()))
        is_continue = False


class Mover(threading.Thread):
    def __init__(self, thread_name: str, prod_buffer: queue.Queue, mov_buffer: queue.Queue, con_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.prod_buffer = prod_buffer
        self.mov_buffer = mov_buffer
        self.con_buffer = con_buffer

    def run(self):
        global is_continue
        while is_continue:
            item = self.prod_buffer.get()
            time.sleep(random.random())
            print('%s : %s is moving %d to the Mover buffer' % (time.ctime(), self.getName(), item))
            self.mov_buffer.put(item)
            time.sleep(random.random())
            item = self.mov_buffer.get()
            print('%s : %s is moving %d to the Consumer buffer' % (time.ctime(), self.getName(), item))
            self.con_buffer.put(item)


class Consumer(threading.Thread):
    def __init__(self, thread_name: str, con_buffer: queue.Queue):
        threading.Thread.__init__(self, name=thread_name)
        self.con_buffer = con_buffer
        self.sum = 0

    def run(self):
        global is_continue
        while is_continue:
            item = self.con_buffer.get()
            print('%s : %s is consuming, %d in the queue is consumed!' % (time.ctime(), self.getName(), item))
            self.sum += item
        print('%s : %s consumer finish, sum is %d' % (time.ctime(), self.getName(), self.sum))


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
