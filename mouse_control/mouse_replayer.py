import time
import pynput
import pickle

class MouseReplayer:
    def __init__(self):
        with open("test_commands.pkl", "rb") as file:
            self.commands = pickle.load(file)

        self.mouse_controller = pynput.mouse.Controller()
        print(self.commands)
        self.replay_commands(self.commands)

    def move(self, x, y):
        print(f"Moving to: {x}, {y}")
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
            if dt>0:
                time.sleep(dt)
            try:
                self.route_command(cmd[1:])
            except TypeError as e:
                print(cmd)
                raise e




MouseReplayer()