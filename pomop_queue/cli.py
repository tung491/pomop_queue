import argparse
from queue import Queue
import csv


def initialize_queue() -> Queue:
    queue = Queue()
    with open('.tasks.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            id_, priority, name = row
            id_ = int(id_)
            priority = int(id_)
            item = (id_, priority, name)
            queue.put(item)
    return queue


def cli():
    argp = argparse.ArgumentParser()
    argp.add_argument('-p', '--print',
                      help='Print all elements in queue',
                      action='')
