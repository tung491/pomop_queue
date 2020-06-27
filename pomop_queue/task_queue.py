from queue import PriorityQueue
import csv
from typing import Tuple
import sqlite3
import operator
from pathlib import Path

db_path = f'{str(Path.home())}/.tasks.db'
conn = sqlite3.connect(db_path)


class Queue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.curr_id = 1

    @property
    def size(self) -> int:
        return self.queue.qsize()

    @staticmethod
    def insert_into_db(item) -> None:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO tasks (id, name, priority)
                       VALUES (?, ?, ?)""", item)
        conn.commit()

    @staticmethod
    def remove_from_db(id_) -> None:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM tasks
        WHERE id=:id""", {'id': id_})
        conn.commit()

    @staticmethod
    def update_into_db(id_: int, name: str = '', priority: int = 0) -> None:
        cursor = conn.cursor()
        sql_query = """UPDATE tasks SET {}=? WHERE ID=?"""
        if name:
            field = 'name'
            field_value = name
        else:
            field = 'priority'
            field_value = priority
        sql_query = sql_query.format(field)
        cursor.execute(sql_query, (field_value, id_))
        conn.commit()

    @staticmethod
    def get_next_popped_item() -> Tuple[int, str, int]:
        cursor = conn.cursor()
        sql_query = '''SELECT * FROM tasks 
        ORDER BY priority asc, id asc 
        LIMIT 1
        '''
        return cursor.execute(sql_query).fetchone()


    def put(self, priority: int, name: str, no_insert: bool = False) -> int:
        item = (self.curr_id, priority, name)
        self.queue.put(item)
        self.curr_id += 1
        if not no_insert:
            self.insert_into_db(item)

    def pop(self) -> str:
        id_, name, priority = self.queue.get()
        self.remove_from_db(id_)
        return name

    def pop_item(self, id_: int) -> Tuple[int, int, str]:
        pop_items = []
        while item := self.queue.get()[0] != id_:
            pop_items.append(item)
        returned_item = item

        for item in pop_items:
            self.queue.put(item)
        self.remove_from_db(id_)
        return returned_item

    def modify_prority(self, id_: int, new_priority: int) -> None:
        item = self.pop_item(id_)
        item = (item[0], new_priority, item[2])
        self.update_into_db(id_, priority=new_priority)
        self.queue.put(item)

    def modify_name(self, id_: int, new_name: str) -> None:
        item = self.pop_item(id_)
        item = (*item[:2], new_name)
        self.queue.put(item)
        self.update_into_db(id_, name=new_priority)

    def remove(self, id_: int) -> None:
        self.pop_item(id_)

    def print(self) -> None:
        print('ID | Name | Priority')
        print('-' * 30)
        for id_, priority, name in sorted(self.queue.queue, key=operator.itemgetter(2, 0)):
            print(f'{id_} | {priority} | {name}')

    def write_to_file(self, mode: str, item: Tuple[int, int, str] = ()) -> None:
        if mode == 'a':
            if not item:
                raise ValueError('Need pass argument item '
                                 'into function when mode is append')
            with open('.tasks.csv', mode) as f:
                writer = csv.writer(f)
                writer.writerow(item)
        elif mode == 'w':
            with open('.task.csv', mode) as f:
                writer = csv.writer(f)
                for item in self.queue.queue:
                    writer.writerow(item)
        else:
            raise ValueError('Invaild mode. Just accept "a" and "w" mode')