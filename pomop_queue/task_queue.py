import operator
import sqlite3
from pathlib import Path
from queue import PriorityQueue
from typing import Tuple

db_path = f'{str(Path.home())}/.tasks.db'

Item = Tuple[int, int, str]


class Queue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.curr_id = 1

    @property
    def size(self) -> int:
        return self.queue.qsize()

    @staticmethod
    def insert_into_db(item: Item) -> None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO tasks (id, priority, name)
                       VALUES (?, ?, ?)""", item)
        conn.commit()
        conn.close()

    @staticmethod
    def remove_from_db(id_) -> None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM tasks
        WHERE id=:id""", {'id': id_})
        conn.commit()
        conn.close()

    @staticmethod
    def update_into_db(id_: int, name: str = '', priority: int = 0) -> None:
        conn = sqlite3.connect(db_path)
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
        conn.close()

    @staticmethod
    def get_item(id_: int) -> Item:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        sql_query = '''SELECT * FROM tasks
        WHERE id=:id
        '''
        item = cursor.execute(sql_query, {'id': id_}).fetchone()
        conn.commit()
        conn.close()
        return item

    @staticmethod
    def get_next_popped_item() -> Item:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        sql_query = '''SELECT * FROM tasks
        ORDER BY priority, id
        LIMIT 1
        '''
        item = cursor.execute(sql_query).fetchone()
        conn.close()
        return item

    def put(self, priority: int, name: str, insert: bool = True, id_: int = -1) -> None:
        if id_ == -1:
            id_ = self.curr_id
        item = (id_, name, priority)
        self.queue.put(item)
        if insert:
            self.curr_id += 1
            self.insert_into_db(item)

    def pop(self) -> Item:
        item = self.queue.get()
        id_, priority, name = item
        self.remove_from_db(id_)
        return item

    def pop_item(self, id_: int) -> Item:
        pop_items = []
        while (item := self.queue.get())[0] != id_:
            pop_items.append(item)
        returned_item = item
        for item in pop_items:
            self.queue.put(item)
        self.remove_from_db(id_)
        return returned_item

    @staticmethod
    def modify_prority(id_: int, new_priority: int) -> None:
        sql_query = '''UPDATE tasks SET priority=:new_priority
        WHERE id=:id
        '''
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query, {'new_priority': new_priority, 'id': id_})
        conn.commit()
        conn.close()

    def modify_name(self, id_: int, new_name: str) -> None:
        item = self.pop_item(id_)
        item = (*item[:2], new_name)
        self.queue.put(item)
        self.update_into_db(id_, name=new_name)

    def remove(self, id_: int) -> None:
        self.pop_item(id_)

    def print(self) -> None:
        print('ID | Name | Priority')
        print('-' * 30)
        print(self.queue.queue)
        sorted_queue = sorted(self.queue.queue, key=operator.itemgetter(1, 0))
        for id_, priority, name in sorted_queue:
            print(f'{id_} | {name} | {priority}')
