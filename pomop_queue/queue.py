from queue import PriorityQueue
from typing import Tuple


class Queue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.curr_id = 1

    @property
    def size(self) -> int:
        return self.queue.qsize()

    def put(self, priority: int, name: str) -> int:
        self.queue.put((self.curr_id, priority, name))
        self.curr_id += 1
        return self.curr_id - 1

    def pop(self) -> str:
        _, _, name = self.queue.get()
        return name

    def pop_item(self, id_: int) -> Tuple[int, int, str]:
        pop_items = []
        while item := self.queue.get()[0] != id_:
            pop_items.append(item)
        returned_item = item

        for item in pop_items:
            self.queue.put(item)
        return returned_item

    def modify_prority(self, id_: int, new_priority: int) -> None:
        item = self.pop_item(id_)
        item = (item[0], new_priority, item[2])
        self.queue.put(item)

    def modify_name(self, id_: int, new_name: str) -> None:
        item = self.pop_item(id_)
        item = (*item[:2], new_name)
        self.queue.put(item)

    def remove(self, id_: int) -> None:
        self.pop_item(id_)

    def print(self) -> None:
        print('ID | Priority | Name')
        print('-' * 30)
        for id_, priority, name in self.queue.queue:
            print(f'{id_} | {priority} | {name}')
