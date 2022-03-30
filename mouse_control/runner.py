#! /usr/bin/env python
from utils.timers import countdown
import signal
from mouse_replayer import MouseReplayer
from mouse_recorder import MouseRecorder
import random
import argparse


class ExitCommand(Exception):
    pass


def signal_handler(signal, frame):
    raise ExitCommand()


class OMRunner:
    def __init__(self):
        signal.signal(signal.SIGUSR1, signal_handler)

    def run(self, iterations):
        try:
            self.run_loop(iterations)
        except ExitCommand:
            print("Exiting from user input")
        finally:
            print("Finished")

    def run_loop(self, iterations):
        for i in range(iterations):
            print(f"Iteration {i + 1}\n======================")
            MouseReplayer("om_entry.pkl")
            sleeptime = 60 + random.random() * 20
            # print(f"Sleeping for {sleeptime} seconds on loop {i}")
            countdown(sleeptime)


class Selector:
    def __init__(self, program):

        # print("What do you want to run?")
        # print("r: Run the recorded program")
        # print("rec: Record the mouse movements")
        # inp = input("")
        if program == "run":
            OMRunner().run(iterations=20)
        elif program == "record":
            MouseRecorder().start()
        else:
            print(f"Input {program} not recognized")




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run some recorded mouse movements")
    parser.add_argument('program', nargs='?', default='run')
    args = parser.parse_args()
    Selector(args.program)
