import time
import pynput
import pickle
import random
from tqdm import tqdm
import sys
from utils.timers import countdown


class MouseReplayer:
    def __init__(self, mouse_file: str):
        with open(mouse_file, "rb") as file:
            self.commands = pickle.load(file)

        self.mouse_controller = pynput.mouse.Controller()
        # print(self.commands)
        self.replay_commands(self.commands)

    def move(self, x, y):
        # print(f"Moving to: {x}, {y}")
        self.mouse_controller.position = (x, y)

    def click(self, x, y, button, press):
        if press:
            self.mouse_controller.press(button)
        else:
            self.mouse_controller.release(button)

    def route_command(self, command):
        cmd = command[0]
        cmd_map = {"move": self.move,
                   "click": self.click}
        cmd_map[cmd](*command[1:])

    def replay_commands(self, commands):
        start_time = time.time()
        for cmd in commands:
            elapsed_time = time.time() - start_time
            dt = cmd[0] - elapsed_time
            if dt > 0:
                time.sleep(dt)
            try:
                self.route_command(cmd[1:])
            except TypeError as e:
                print(cmd)
                raise e


for i in range(10):
    print(f"Iteration {i + 1}\n======================")
    MouseReplayer("om_entry.pkl")
    sleeptime = 60 + random.random() * 20
    # print(f"Sleeping for {sleeptime} seconds on loop {i}")
    countdown(sleeptime)

    # time.sleep(sleeptime)
print("Finished")
