import argparse
import shlex
import sqlite3
import sys
from pathlib import Path
from subprocess import Popen

from task_queue import Queue


def initialize_queue() -> Queue:
    queue = Queue()
    conn = sqlite3.connect(f"{str(Path.home())}/.tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
    (id int PRIMARY KEY,
    priority int,
    name varchar
    );
    ''')
    tasks = cursor.execute('''SELECT * FROM tasks
    ORDER BY priority asc, id asc;
    ''').fetchall()
    for task in tasks:
        queue.put(*task[1:], no_insert=True)
    queue.curr_id = task[0] + 1
    return queue


def cli() -> None:
    queue = initialize_queue()

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='sub-command help', dest='branchs')

    # Parser for queue
    queue_parser = subparser.add_parser('queue', help='queue help')
    queue_subparse = queue_parser.add_subparsers(help='Queue options help',
                                                 dest='queue_cmd')

    queue_subparse.add_parser('list', help='List all tasks in queue')
    queue_subparse.add_parser('size', help='Size of the task queue')
    rm_parse = queue_subparse.add_parser('rm',
                                         help='Remove element from task queue')
    rm_parse.add_argument('id', help='The id of element want to remove',
                          type=int)

    add_parser = queue_subparse.add_parser('add',
                                           help='Add task into task queue')
    add_parser.add_argument('name', help='Name of the task')
    add_parser.add_argument('priority',
                            help='The priority number of the task (1 - 5).'
                                 '1 is the highest priority level,'
                                 '5 is the lowest one.'
                                 'Default is 3',
                            default=3, type=int)

    modify_name_parser = queue_subparse.add_parser('modify_name',
                                                   help='Modify the name of task')
    modify_name_parser.add_argument('id', help='The ID of the task', type=int)
    modify_name_parser.add_argument('name', help='The new name of the task',
                                    type=str)

    modify_priority_parser = queue_subparse.add_parser('modify_priority',
                                                       help='Modify the priority of the task')
    modify_priority_parser.add_argument('id', help='The ID of the task',
                                        type=int)
    modify_priority_parser.add_argument('priority',
                                        help='The new level priority of the task',
                                        type=int)

    # Parser for pomop
    pomop_parser = subparser.add_parser('pomop', help='pomop help')
    pomop_subparser = pomop_parser.add_subparsers(dest='pomop_cmd')
    pomop_subparser.add_parser('next-task')
    pomop_parser.add_argument('-l', '--length',
                              help='Length in minutes of this pomodoro',
                              default=25, type=int)
    pomop_parser.add_argument('-S', '--nosound',
                              help='Turn off sound notification',
                              action='store_false')
    pomop_parser.add_argument('-B', '--nobrowser',
                              help='Turn off browser-open notification',
                              action='store_false')
    pomop_parser.add_argument('--target_id',
                              help='Target ID of the pomodoro. Default the next '
                                   'popped element in the queue',
                              type=int, default=0)
    args = parser.parse_args()
    if not args.branchs:
        parser.print_help()
    elif args.branchs == 'queue':
        if not args.queue_cmd:
            queue_parser.print_help()
        elif args.queue_cmd == 'list':
            queue.print()
        elif args.queue_cmd == 'get_size':
            print(queue.size)
        elif args.queue_cmd == 'rm':
            queue.remove(args.id)
        elif args.queue_cmd == 'add':
            queue.put(args.priority, args.name)
        elif args.queue_cmd == 'modify_name':
            queue.put(args.id, args.name)
        elif args.queue_cmd == 'modify_priority':
            queue.put(args.id, args.priority)
    elif args.branchs == 'pomop':
        options = []
        if args.pomop_cmd == 'next-task':
            item = queue.get_next_popped_item()
            print('ID | Name | Priority')
            print('{} | {} | {}'.format(*item))
            sys.exit()
        else:
            if args.length:
                options.append(f'-l {args.length}')
            if args.nosound:
                options.append('-S')
            if args.nobrowser:
                options.append('-B')
            if args.target_id < 0 or args.target_id >= queue.curr_id:
                raise ValueError('Invaild target id')
        name = queue.pop() if not args.target_id else queue.pop_item(
            args.target_id)
        str_options = ' '.join(options)
        cmd = f'pomop {str_options} {name}'
        Popen(shlex.split(cmd))


if __name__ == '__main__':
    cli()
