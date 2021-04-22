from __future__ import annotations
import tkinter as tk

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

    def __hash__(self):
        return hash(tuple(self.pos.tolist()))


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, pos):
        self.nodes.append(Node(pos))
        return self.nodes[-1]

    def get_node(self, pos: np.ndarray):
        for node in self.nodes:
            if all(np.abs(node.pos - pos) <= 0.01):
                return node
        return None

    def get_or_add_node(self, pos: np.ndarray):
        if node := self.get_node(pos):
            return node
        return self.add_node(pos)

    def add_edge(self, n1, n2):
        n1.successors.append(n2)


def merge_graphs(g1: Graph, g2: Graph):
    for n1 in g1.nodes:
        if n2 := g2.get_node(n1.pos):
            n1.successors += n2.successors
            g2.nodes.remove(n2)
            for n3 in g2.nodes:
                n3.successors = [n1 if suc is n2 else suc for suc in n3.successors]


class RingGraph(Graph):
    def __init__(self, center, radius=300, num_nodes=24, reverse=False):
        super().__init__()

        angles = np.linspace(0, 2 * np.pi, num=num_nodes + 1)[0:-1]
        vals = [(np.sin(th), np.cos(th)) for th in angles]

        if reverse:
            vals.reverse()

        for val in vals:
            self.add_node(radius * np.array(val) + np.array(center))

        for n1, n2 in zip(self.nodes, self.nodes[1:]):
            self.add_edge(n1, n2)
        self.add_edge(self.nodes[-1], self.nodes[0])


class ThreeRingGraph(Graph):
    def __init__(self, center, radii=200, num_nodes_per_circle=24):
        super().__init__()
        self.make_three_rings(center, radii, num_nodes_per_circle)

    def make_three_rings(self, center, radii, num_nodes_per_circle):

        h = -np.sqrt(3) * radii
        offset = -np.tan(np.deg2rad(30)) * radii
        c1 = np.array(center) + np.array([0, h - offset])
        c2 = np.array(center) + np.array([radii, -offset])
        c3 = np.array(center) + np.array([-radii, -offset])

        # for center in [c1, c2, c3]:
        # self.add_ring(center, radii, num_nodes_per_circle)
        r1 = RingGraph(c1, radii, num_nodes_per_circle)
        r1_m = RingGraph(c1, radii, num_nodes_per_circle, reverse=True)
        r2 = RingGraph(c2, radii, num_nodes_per_circle)
        r2_m = RingGraph(c2, radii, num_nodes_per_circle, reverse=True)
        r3 = RingGraph(c3, radii, num_nodes_per_circle)
        r3_m = RingGraph(c3, radii, num_nodes_per_circle, reverse=True)

        merge_graphs(r1, r2_m)
        # merge_graphs(r2, r3_m)
        # merge_graphs(r3, r1_m)
        merge_graphs(r1, r3_m)
        # merge_graphs(r2, r1_m)
        # merge_graphs(r3, r2_m)

        for g in [r1, r2_m, r3_m]:
            self.nodes += g.nodes

        # for g in [r1, r2, r3, r1_m, r2_m, r3_m]:
        #     self.nodes += g.nodes




    def add_ring(self, center, radius, num_nodes):
        angles = np.linspace(0, 2 * np.pi, num=num_nodes + 1)[0:-1]
        vals = [(np.sin(th), np.cos(th)) for th in angles]
        new_nodes = []
        for val in vals:
            pos = radius * np.array(val) + np.array(center)
            if node := self.get_node(pos):
                pass
            else:
                node = self.add_node(pos)

            new_nodes.append(node)
        for n1, n2 in zip(new_nodes, new_nodes[1:]):
            self.add_edge(n1, n2)
        self.add_edge(new_nodes[-1], new_nodes[0])


class Agent:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.cur_node = None
        self.period = 10
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
        self.cur_node = np.random.choice(suc)
        # self.cur_node = suc[0]
        # raise RuntimeError("Undefined behavior for multiple successors")


class LEDArray:
    default_color = "#222222"
    active_color = "red"

    def __init__(self, graph: Graph, canvas: tk.Canvas):
        # unique_poses = {n.pos for n in graph.nodes}

        self.node_to_led = dict()
        self.led_handles = []

        for n in graph.nodes:
            key_n = tuple(n.pos.tolist())
            for k, v in self.node_to_led.items():
                if np.all(np.array(k) - n.pos <= 0.01):
                    self.node_to_led[key_n] = v
                    break
            self.led_handles.append(create_circle(canvas, n, fill=self.default_color))
            self.node_to_led[key_n] = len(self.led_handles) - 1


        #
        # for n in graph.nodes:
        #     k = n.pos.tolist()
        #     if k in self.led_handles:
        #         continue
        #     self.led_handles[k] = create_circle(canvas, n, fill=self.default_color)

        # {n: create_circle(canvas, n, fill=self.default_color) for n in graph.nodes}

    def update(self, canvas: tk.Canvas, active_nodes):
        for k, v in self.node_to_led.items():
            if k in [tuple(n.pos.tolist()) for n in active_nodes]:
                canvas.itemconfig(self.led_handles[v], fill=self.active_color)
            else:
                canvas.itemconfig(self.led_handles[v], fill=self.default_color)


class RingSculpture:
    def __init__(self, parent):
        self.seconds = 0
        self.canvas = tk.Canvas(parent, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()

        # tk.Canvas.create_circle_arc = _create_circle_arc

        # create_circle(self.canvas, 100, 120, 50, fill="blue", outline="#DDD", width=4)
        # self.c2 = create_circle(self.canvas, 150, 40, 20, fill="#BBB", outline="")

        self.graph = ThreeRingGraph(center=(500, 500))
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
