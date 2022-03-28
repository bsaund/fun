import time
import pynput
import pickle
import os
import signal
from tqdm import tqdm
import sys


class MouseReplayer:
    def __init__(self, mouse_file: str):

        self.keyboard_listener = pynput.keyboard.Listener(
            on_press=self.on_press)

        self.keyboard_listener.start()

        with open(mouse_file, "rb") as file:
            self.commands = pickle.load(file)

        self.mouse_controller = pynput.mouse.Controller()
        # print(self.commands)
        self.replay_commands(self.commands)

    def on_press(self, key):
        print(f"A key was pressed: {key}")
        if key == pynput.keyboard.Key.esc:
            print("Raising exception")
            os.kill(os.getpid(), signal.SIGUSR1)
            # raise os._exit(1)

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
