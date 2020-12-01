# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy
import time
import math
import heapq
from queue import PriorityQueue


def wip_pqueue():
    q = PriorityQueue()
    q.put((1, "a"))
    q.put((2, "b"))
    q.put((1.5, "c"))

    while not q.empty():
        print(q.get())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wip_pqueue()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
