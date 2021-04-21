import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
from collections import defaultdict


def create_circle_base(c, x, y, r, **kwargs):
    return c.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def create_circle(canvas, node, **kwargs):
    return create_circle_base(canvas, node.pos[0], node.pos[1], node.r, **kwargs)


class Node:

    def __init__(self, pos: np.ndarray, radius=5):
        self.pos = pos
        self.r = radius
        self.successors = []


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, pos):
        self.nodes.append(Node(pos))
        return self.nodes[-1]

    def get_or_add_node(self, pos: np.ndarray):
        for node in self.nodes:
            if all(node.pos == pos):
                return node
        self.nodes.append(Node(pos))

    def add_edge(self, n1, n2):
        n1.successors.append(n2)


class RingGraph(Graph):
    def __init__(self, center, radius=300, num_nodes=24):
        super().__init__()

        angles = np.linspace(0, 2 * np.pi, num=num_nodes + 1)[0:-1]
        vals = [(np.sin(th), np.cos(th)) for th in angles]

        for val in vals:
            self.add_node(radius * np.array(val) + np.array(center))

        for n1, n2 in zip(self.nodes, self.nodes[1:]):
            self.add_edge(n1, n2)
        self.add_edge(self.nodes[-1], self.nodes[0])

class ThreeRingGraph(Graph):
    def __init__(self):
        super().__init__()
        self.nodes


class Agent:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.cur_node = None
        self.period = 20
        self.cur_node_count = 0

    def update(self, graph: Graph):
        if self.cur_node is None:
            self.cur_node = graph.nodes[0]

        self.cur_node_count += 1
        if self.cur_node_count < self.period:
            return

        self.cur_node_count = 0
        suc = self.cur_node.successors
        if len(suc) == 0:
            raise RuntimeError("Node has no successors")
        if len(suc) == 1:
            self.cur_node = suc[0]
            return
        raise RuntimeError("Undefined behavior for multiple successors")


class LEDArray:
    default_color = "#222222"
    active_color = "red"

    def __init__(self, graph: Graph, canvas: tk.Canvas):
        self.led_handles = {n: create_circle(canvas, n, fill=self.default_color) for n in graph.nodes}

    def update(self, canvas: tk.Canvas, active_nodes):
        for k, v in self.led_handles.items():
            if k in active_nodes:
                canvas.itemconfig(v, fill=self.active_color)
            else:
                canvas.itemconfig(v, fill=self.default_color)


class RingSculpture:
    def __init__(self, parent):
        self.seconds = 0
        self.canvas = tk.Canvas(parent, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()

        # tk.Canvas.create_circle_arc = _create_circle_arc

        # create_circle(self.canvas, 100, 120, 50, fill="blue", outline="#DDD", width=4)
        # self.c2 = create_circle(self.canvas, 150, 40, 20, fill="#BBB", outline="")

        self.graph = RingGraph(center=(500, 500))
        self.leds = LEDArray(self.graph, self.canvas)
        self.agents = [Agent()]

        parent.wm_title("Circles and Arcs")

        self.label = tk.Label(parent, text="0 s", font="Arial 30", width=10)
        self.label.pack()

        self.label.after(1000, self.refresh_label)

    def refresh_label(self):
        """ refresh the content of the label every second """

        for agent in self.agents:
            agent.update(self.graph)

        self.leds.update(self.canvas, active_nodes=[agent.cur_node for agent in self.agents])

        self.seconds += 0.010
        self.label.configure(text=f"{self.seconds:0.3f} s")
        self.label.after(10, self.refresh_label)
        # self.graph.update(self.canvas)


if __name__ == "__main__":
    # make_sin_graph(root)
    # make_quit_button()
    # root = tkinter.Tk()
    # repeated()
    root = tk.Tk()
    root.wm_title("Testing Tkinter")
    RingSculpture(root)
    root.mainloop()
