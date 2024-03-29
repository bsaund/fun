import tkinter as tk
import numpy as np

DEBUG = False


class Params:
    nodes_per_circle = 18
    common_period_bounds = [10, 80]
    common_period_change_rate = 1
    global_update_period_ms = 1000
    individual_period_factor_bounds = [1.0, 1.5]
    individual_period_factor_change_rate = 0.001
    decision_resampling_period = 100


def create_circle_base(c, x, y, r, **kwargs):
    return c.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def create_circle(canvas, node, **kwargs):
    return create_circle_base(canvas, node.pos[0], node.pos[1], node.r, **kwargs)


node_counter = 0


class Node:
    def __init__(self, pos: np.ndarray, radius=5):
        global node_counter
        self.pos = pos
        self.r = radius
        self.successors = []
        self.id = node_counter
        node_counter += 1
        self.sampler = None

    def sample_successor(self):
        if len(self.successors) == 1:
            return self.successors[0]
        if len(self.successors) == 0:
            raise RuntimeError("Node has no successors")
        if len(self.successors) > 2:
            raise RuntimeError(f"Node has {len(self.successors)} successors. Only 1 or 2 supported")

        if self.sampler is None:
            self.sampler = BinaryDecision()

        return self.sampler.choose(self.successors)

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"id: {self.id}. pos: {self.pos}."


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

    @staticmethod
    def add_edge(n1, n2):
        n1.successors.append(n2)


def merge_graphs(g1: Graph, g2: Graph):
    for n1 in g1.nodes:
        if n2 := g2.get_node(n1.pos):
            n1.successors += n2.successors
            g2.nodes.remove(n2)
            for n3 in g2.nodes:
                n3.successors = [n1 if suc is n2 else suc for suc in n3.successors]


class RingGraph(Graph):
    def __init__(self, center, radius, num_nodes, reverse=False):
        super().__init__()

        angles = np.linspace(0, 2 * np.pi, num=num_nodes + 1)[0:-1]
        vals = [(np.cos(th), np.sin(th)) for th in angles]

        if reverse:
            vals.reverse()

        for val in vals:
            self.add_node(radius * np.array(val) + np.array(center))

        for n1, n2 in zip(self.nodes, self.nodes[1:]):
            self.add_edge(n1, n2)
        self.add_edge(self.nodes[-1], self.nodes[0])


class ArcGraph(Graph):
    def __init__(self, center, radius, num_nodes, start_angle_deg=0, end_angle_deg=0, reverse=False):
        super().__init__()
        angles = np.linspace(np.deg2rad(start_angle_deg), np.deg2rad(end_angle_deg), num=num_nodes + 1)
        vals = [(np.cos(th), np.sin(th)) for th in angles]
        if reverse:
            vals.reverse()

        for val in vals:
            self.add_node(radius * np.array(val) + np.array(center))
        for n1, n2 in zip(self.nodes, self.nodes[1:]):
            self.add_edge(n1, n2)


class ThreeRingGraph(Graph):
    def __init__(self, center, radii=200, num_nodes_per_circle=18):
        super().__init__()
        self.make_three_rings(center, radii, num_nodes_per_circle)

    def make_three_rings(self, center, radii, num_nodes_per_circle):
        forwards = []
        mirrors = []
        center = np.array(center)

        def add_circle_pair(cir_center):
            forwards.append(RingGraph(cir_center, radii, num_nodes_per_circle))
            mirrors.append(RingGraph(cir_center, radii, num_nodes_per_circle, reverse=True))

        def add_arc_pair(arc_center, start_deg, end_deg):
            num_nodes = num_nodes_per_circle * (end_deg - start_deg) / 360
            if not num_nodes.is_integer():
                raise RuntimeError(f"Configuration invalid. Trying to build an arc with {num_nodes} nodes")
            forwards.append(ArcGraph(arc_center, radii, int(num_nodes), start_deg, end_deg))
            mirrors.append(ArcGraph(arc_center, radii, int(num_nodes), start_deg, end_deg, reverse=True))

        # Circle Centers
        h = -np.sqrt(3) * radii
        offset = -np.tan(np.deg2rad(30)) * radii
        c1 = center + [0, h - offset]
        c2 = center + [radii, -offset]
        c3 = center + [-radii, -offset]

        for c in [c1, c2, c3]:
            add_circle_pair(c)

        # Arc Centers
        c4 = center + [-2 * radii, h - offset]
        c5 = center + [2 * radii, h - offset]
        c6 = center + [0, -offset - h]

        add_arc_pair(c4, 0, 60)
        add_arc_pair(c5, 120, 180)
        add_arc_pair(c6, -120, -60)

        for i, f in enumerate(forwards):
            for j, r in enumerate(mirrors):
                if i == j:
                    continue
                merge_graphs(f, r)

        for g in forwards + mirrors:
            self.nodes += g.nodes


class BinaryDecision:
    def __init__(self):
        self.left_prob = 0.5
        self.sample_decision_probability()
        self.visit_count = 0

    def sample_decision_probability(self):
        self.left_prob = np.random.choice([0.1, 0.9])
        print(f"Binary decision with prob {self.left_prob}")

    def choose(self, choices):
        self.visit_count += 1
        p = Params()
        if self.visit_count > p.decision_resampling_period:
            self.visit_count = 0
            self.sample_decision_probability()

        if len(choices) != 2:
            raise RuntimeError(f"Binary Decision must have 2 choices. {len(choices)} provided")

        if np.random.rand() < self.left_prob:
            return choices[0]
        return choices[1]


class Agent:
    def __init__(self):
        p = Params()
        self.pos = np.array([0, 0])
        self.cur_node = None
        self.common_period = 1
        self.individual_period_factor = np.random.uniform(*p.individual_period_factor_bounds)
        self.cur_node_count = 0
        self.node_to_decision = dict()

    def update(self, graph: Graph):
        if self.cur_node is None:
            self.cur_node = graph.nodes[0]

        self.cur_node_count += 1
        if self.cur_node_count < self.common_period * self.individual_period_factor:
            return

        self.cur_node_count = 0
        self.cur_node = self.cur_node.sample_successor()


class LEDArray:
    default_color = "#111111"
    # default_color = "#444444"
    active_color = "red"

    def __init__(self, graph: Graph, canvas: tk.Canvas):
        self.node_to_led = dict()
        self.led_handles = []
        self.active_leds = []
        self.first_pass = True

        for n in graph.nodes:
            for existing_node, led_index in self.node_to_led.items():
                if np.all(np.abs(existing_node.pos - n.pos) <= 0.01):
                    self.node_to_led[n] = led_index
                    break
            if n not in self.node_to_led:
                self.led_handles.append(create_circle(canvas, n, fill=self.default_color))
                self.node_to_led[n] = len(self.led_handles) - 1
        print(f"{len(self.led_handles)} leds create")

    def update(self, canvas: tk.Canvas, active_nodes):

        previously_active_leds = self.active_leds
        self.active_leds = {self.node_to_led[n] for n in active_nodes}

        if previously_active_leds == self.active_leds:
            return

        for led_index, led in enumerate(self.led_handles):
            if led_index in self.active_leds:
                continue
            if not self.first_pass and led_index not in previously_active_leds:
                continue

            canvas.itemconfig(led, fill=self.default_color)
            # canvas.itemconfig(led, state='hidden')

        for led_index in self.active_leds:
            led = self.led_handles[led_index]
            canvas.itemconfig(led, state='normal')
            canvas.itemconfig(led, fill=self.active_color)

        self.first_pass = False


class RingSculpture:
    def __init__(self, parent):
        p = Params()
        self.common_period = np.random.randint(*p.common_period_bounds)
        # self.common_period = np.max(p.common_period_bounds)

        self.seconds = 0
        self.canvas = tk.Canvas(parent, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="black")
        parent.attributes("-fullscreen", True)
        parent["bg"] = "black"
        self.canvas.pack()

        # print("making graph")
        self.graph = ThreeRingGraph(center=(500, 500), num_nodes_per_circle=p.nodes_per_circle)
        # print("making led array")
        self.leds = LEDArray(self.graph, self.canvas)
        # print("Making agent")
        self.agents = [Agent(), Agent()]

        parent.wm_title("Circles and Arcs")

        if DEBUG:
            self.label = tk.Label(parent, text="0 s", font="Arial 30", width=10)
            self.label.pack()

        self.canvas.after(10, self.refresh_pane)
        self.canvas.after(1, self.global_update)
        parent.bind('<Escape>', self.quit)
        parent.bind('q', self.quit)

    def global_update(self):
        p = Params()

        self.common_period += np.random.randint(-p.common_period_change_rate, 1 + p.common_period_change_rate)
        self.common_period = np.clip(self.common_period, *p.common_period_bounds)

        for agent in self.agents:
            cr = p.individual_period_factor_change_rate
            agent.individual_period_factor += np.random.uniform(-cr, cr)
            agent.individual_period_factor = np.clip(agent.individual_period_factor, *p.individual_period_factor_bounds)

        print(f"Global Update. Period {self.common_period}")

        for agent in self.agents:
            agent.common_period = self.common_period
        self.canvas.after(p.global_update_period_ms, self.global_update)

    def refresh_pane(self):
        for agent in self.agents:
            agent.update(self.graph)

        self.leds.update(self.canvas, active_nodes=[agent.cur_node for agent in self.agents])

        self.seconds += 0.001
        if DEBUG:
            self.label.configure(text=f"{self.seconds:0.3f} s")
        self.canvas.after(1, self.refresh_pane)

    def quit(self, _event=None):
        print("Calling it quits")
        self.canvas.quit()
        self.canvas.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Testing Tkinter")
    RingSculpture(root)
    root.mainloop()
