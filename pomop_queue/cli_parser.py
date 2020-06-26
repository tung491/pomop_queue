import argparse
from task_queue import Queue
import csv


def initialize_queue() -> Queue:
    queue = Queue()
    try:
        with open('~/.tasks.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                id_, priority, name = row
                id_ = int(id_)
                priority = int(id_)
                item = (id_, priority, name)
                queue.put(item)
    except FileNotFoundError:
        pass
    return queue


def cli():
    queue = initialize_queue()

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='sub-command help')

    queue_parser = subparser.add_parser('queue', help='queue help')
    queue_subparse = queue_parser.add_subparsers(help='Queue options help')

    list_parser = queue_subparse.add_parser('list', help='List all tasks in queue')
    size_parser = queue_subparse.add_parser('size', help='Size of the task queue')
    rm_parse = queue_subparse.add_parser('rm', help='Remove elememt from task queue')
    rm_parse.add_argument('id', help='The id of element want to remove', type=int)

    add_parser = queue_subparse.add_parser('add', help='Add task into ')
    add_parser.add_argument('name', help='Name of the task')
    add_parser.add_argument('priority', help='The priority number of the task (1 - 5).'
                                             '1 is the highest priority level,'
                                             '5 is the lowest one.'
                                             'Default is 3',
                            default=3, type=int)

    modify_name_parser = queue_subparse.add_parser('modify_name', help='Modify the name of task')
    modify_name_parser.add_argument('id', help='The ID of the task', type=int)
    modify_name_parser.add_argument('name', help='New name of the task', type=str)

    args = parser.parse_args(['queue', 'list'])


if __name__ == '__main__':
    cli()
