import time
import pynput
import pickle
import os
import signal
from tqdm import tqdm
import sys


SINGLE_TILE_WIDTH = 8
SINGLE_ROOM = 4
CONDO_WIDTH = 16
ONE_FLOOR_HEIGHT = -36

DY = ONE_FLOOR_HEIGHT
# DX = CONDO_WIDTH
DX = SINGLE_ROOM
DX *= -SINGLE_TILE_WIDTH

class MouseReplayer:
    def __init__(self):
        self.keyboard_listener = pynput.keyboard.Listener(
            on_press=self.on_press)
        self.keyboard_listener.start()
        self.mouse_controller = pynput.mouse.Controller()
        self.mouse_file = "saved_mouse_movements/set_sim_tower_elevator.pkl"
        # print(self.commands)
        # self.replay_commands(selfelf.commands)
    def join(self):
        self.keyboard_listener.join()

    def on_press(self, key):
        print(f"A key was pressed: {key}")
        if key == pynput.keyboard.Key.esc:
            print("Raising exception")
            os.kill(os.getpid(), signal.SIGUSR1)
            # raise os._exit(1)
        if key.char == 'u':
            self.run_clicking_upwards()
        if key.char == "l":
            self.run_clicking_leftwards()
        if key.char == "b":
            self.run_clicking_both()
        if key.char == "e":
            with open(self.mouse_file, "rb") as file:
                commands = pickle.load(file)
            self.replay_commands(commands, speed_ratio=2.0)

    def move(self, x, y):
        # print(f"Moving to: {x}, {y}")
        self.mouse_controller.position = (x, y)

    def click(self, x, y, button, press):
        if press:
            self.mouse_controller.press(button)
        else:
            self.mouse_controller.release(button)

    def run_clicking_upwards(self):
        x_init, y_init = self.mouse_controller.position
        x = x_init
        y = y_init
        print(f"Current mouse position is {x}, {y}")
        for i in range(4):
            self.click(x, y, button=pynput.mouse.Button.left, press=True)
            self.click(x, y, button=pynput.mouse.Button.left, press=False)
            y += DY
            self.move(x, y)
            time.sleep(0.2)
        self.move(x_init + DX, y_init)

    def run_clicking_leftwards(self):
        x, y = self.mouse_controller.position
        print(f"Current mouse position is {x}, {y}")
        for i in range(4):
            self.click(x, y, button=pynput.mouse.Button.left, press=True)
            self.click(x, y, button=pynput.mouse.Button.left, press=False)
            x += DX
            self.move(x, y)
            time.sleep(0.2)

    def run_clicking_both(self):
        starting_x, starting_y = self.mouse_controller.position
        y = starting_y
        for j in range(14):
            x = starting_x
            if j > 0:
                y += DY
            for _ in range(8):
                self.move(x, y)
                time.sleep(0.05)
                self.click(x, y, button=pynput.mouse.Button.left, press=True)
                self.click(x, y, button=pynput.mouse.Button.left, press=False)
                # time.sleep(0.05)
                x += DX
                self.move(x, y)
                time.sleep(0.05)
        y = starting_y
        self.move(x,y)


    def route_command(self, command):
        cmd = command[0]
        cmd_map = {"move": self.move,
                   "click": self.click}
        cmd_map[cmd](*command[1:])

    def replay_commands(self, commands, speed_ratio=1.0):
        start_time = time.time()
        for cmd in commands:
            elapsed_time = time.time() - start_time
            dt = cmd[0] - elapsed_time * speed_ratio
            if dt > 0:
                time.sleep(dt)
            try:
                self.route_command(cmd[1:])
            except TypeError as e:
                print(cmd)
                raise e

if __name__ == "__main__":
    mr = MouseReplayer()
    mr.join()