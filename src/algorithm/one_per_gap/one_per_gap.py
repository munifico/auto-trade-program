import queue
from algorithm.one_per_gap.consumer import Consumer
from algorithm.one_per_gap.producer import Producer

q = queue.Queue()


def one_per_gap_start(access, secret, ticker):
    Producer(access, secret, ticker, q).start()
    Consumer(access, secret, ticker, q).start()
