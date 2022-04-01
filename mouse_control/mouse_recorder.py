# import pyautogui as pg
import time
import pynput
import pickle
from utils.timestamp import timestamp


class MouseRecorder:
    def __init__(self):
        self.kb_listener = None
        self.mouse_listener = None
        self.start_time = None
        self.commands = []

    def dt(self):
        return time.time() - self.start_time

    def add_command(self, cmd_tuple):
        command = (self.dt(), ) + cmd_tuple
        print(command)
        self.commands.append(command)

    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        command = ('move', x, y)
        self.add_command(command)

    def on_click(self, x, y, button, pressed):
        # print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        command = ('click', x, y, button, pressed)
        self.add_command(command)

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

    def on_press(self, key):
        print('{0} pressed'.format(key))

    def on_release(self, key):
        print('{0} release'.format(key))
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            return False

    #
    # def record_mouse_position
    #
    # # Collect events until released
    def start(self):
        self.start_time = time.time()
        self.mouse_listener = pynput.mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        self.mouse_listener.start()

        with pynput.keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

        filename = f"mouse_movements/mouse_{timestamp()}.pkl"
        with open(filename, "wb") as file:
            pickle.dump(self.commands, file)
        print(f"Wrote {filename}")


# Collect events until released
# with pynput.mouse.Listener(
#         on_move=on_move,
#         on_click=on_click,
#         on_scroll=on_scroll) as listener:
#     listener.join()
#
# # ...or, in a non-blocking fashion:
# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll)
# listener.start()

if __name__ == "__main__":
    mr = MouseRecorder()
    mr.start()
