from typing import Mapping

tmp_input = [int(a) for a in "389125467"]
actual_input = [int(a) for a in "789465123"]
# p1 = tmp_input.copy()
p1 = actual_input.copy()


def select_head(arr: list, ind: int):
    while ind > 0:
        arr.append(arr.pop(0))
        ind -= 1


def move(arr):
    print(f'cups: {arr}')
    picked = [arr.pop(1), arr.pop(1), arr.pop(1)]
    print(f'picked: {picked}')
    destination = arr[0] - 1
    while destination not in arr:
        destination -= 1
        if destination < min(arr):
            destination = max(arr)
    print(f'destination: {destination}')
    ind = arr.index(destination) + 1
    arr.insert(ind, picked[2])
    arr.insert(ind, picked[1])
    arr.insert(ind, picked[0])
    select_head(arr, 1)


# for i in range(1, 101):
#     print(f'-- move {i} --')
#     move(p1)
#     print()
#
# select_head(p1, p1.index(1))
# print(p1)
# print(''.join([f'{a}' for a in p1])[1:])


# Part 2
print("Part 2")
p2 = p1 + [i for i in range(10, 1000001)]


class Node:
    next = None
    data: int

    def __init__(self, data: int):
        self.data = data


class MappedCircularLinkedList:
    head: Node = None
    tail: Node = None
    map: Mapping[int, Node] = dict()

    def pop(self) -> int:
        if self.head is None:
            raise IndexError("linked list is empty")
        self.head = self.head.next
        return self.head.data

    def append(self, val: int):
        if self.head is None:
            self.head = Node(val)
            self.tail = self.head
        else:
            prev_tail = self.tail
            self.tail = Node(val)
            prev_tail.next = self.tail
        self.tail.next = self.head
        self.map[val] = self.tail

    def get_node_with_value(self, val: int):
        return self.map[val]

    def __repr__(self):
        node = self.head
        count = 0
        vals = [f'{node.data}']
        while node.next is not self.head:
            vals.append(f'{node.next.data}')
            node = node.next
            count += 1
            if count > 15:
                vals.append('...')
                break
        return ", ".join(vals)


def move(cups: MappedCircularLinkedList):
    # print(f'cups: {cups}')
    # Pick up three cups
    picked = cups.head.next
    cups.head.next = cups.head.next.next.next.next
    picked_vals = [picked.data, picked.next.data, picked.next.next.data]
    # print(f'picked up: {picked_vals}')
    # print(f'cups: {cups}')
    destination = cups.head.data - 1
    while destination in picked_vals or destination < 1:
        destination -= 1
        if destination < 1:
            destination = max(cups.map)
    # print(f'destination: {destination}')
    # Insert
    left_of_insertion = cups.map[destination]
    picked.next.next.next = left_of_insertion.next
    left_of_insertion.next = picked

    # select new current cup
    cups.head = cups.head.next


def run_part_2():
    cups = MappedCircularLinkedList()
    for val in p2:
        cups.append(val)
    for i in range(1, 10000000 + 1):
        if i % 1000000 == 0:
            print(f'-- move {i} --')
        move(cups)
    cups.head = cups.map[1]
    print(f'final cups: {cups}')
    print(f'Part 2 answer: {cups.head.next.data * cups.head.next.next.data}')


run_part_2()
