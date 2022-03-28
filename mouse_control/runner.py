from utils.timers import countdown
import signal
from mouse_replayer import MouseReplayer
from mouse_recorder import MouseRecorder
import random


class ExitCommand(Exception):
    pass


def signal_handler(signal, frame):
    raise ExitCommand()


class OMRunner:
    def __init__(self):
        signal.signal(signal.SIGUSR1, signal_handler)

    def run(self):
        try:
            self.run_loop()
        except ExitCommand:
            print("Exiting from user input")
        finally:
            print("Finished")

    def run_loop(self):
        for i in range(10):
            print(f"Iteration {i + 1}\n======================")
            MouseReplayer("om_entry.pkl")
            sleeptime = 60 + random.random() * 20
            # print(f"Sleeping for {sleeptime} seconds on loop {i}")
            countdown(sleeptime)


class Selector:
    def __init__(self):

        print("What do you want to run?")
        print("r: Run the recorded program")
        print("rec: Record the mouse movements")
        inp = input("")
        if inp is "r":
            OMRunner().run()
        elif inp == "rec":
            MouseRecorder().start()
        else:
            print(f"Input {inp} not recognized")


if __name__ == "__main__":
    Selector()
