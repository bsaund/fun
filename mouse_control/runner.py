#! /usr/bin/env python

from utils.timers import countdown
import signal
from mouse_replayer import MouseReplayer
from mouse_recorder import MouseRecorder
from screen_capture import screen_matches, verify_screen_matches, ScreenDoesNotMatchException
import random
import argparse
import time
from typing import List


class ExitCommand(Exception):
    pass


def signal_handler(signal, frame):
    raise ExitCommand()


class RecaptchaChallengeException(Exception):
    pass

class LogicError(Exception):
    pass


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
            self.run_once()
            sleeptime = 60 + random.random() * 20
            # print(f"Sleeping for {sleeptime} seconds on loop {i}")
            countdown(sleeptime)

    def wait_and_verify(self, fn: str):
        now = time.time()
        filename = f"saved_screen_captures/{fn}"
        while not screen_matches(filename):
            time.sleep(0.5)
            if time.time() - now > 30:
                verify_screen_matches(filename)
                break

    def wait_for_any(self, filenames: List[str]):
        now = time.time()
        full_filenames = [f"saved_screen_captures/{fn}" for fn in filenames]

        def check(fns):
            for i, fn in enumerate(fns):
                if screen_matches(fn):
                    return i
            return -1

        ans = check(full_filenames)
        while ans < 0:
            if time.time() - now > 60:
                raise ScreenDoesNotMatchException()
            time.sleep(0.5)
            ans = check(full_filenames)
        return ans

    def check_recaptcha(self):
        possible_screens = ["Happy_reCAPTCHA_solved.pkl",
                            "reCAPTCHA_challenge_verify.pkl",
                            "only_once_a_minute_ready.pkl"]
        match = self.wait_for_any(possible_screens)
        if match >= len(possible_screens):
            print("Unknown screen after clicking on the recaptcha")
            raise ScreenDoesNotMatchException()
        if possible_screens[match] == "reCAPTCHA_challenge_verify.pkl":
            print("Cannot solve recaptcha")
            raise RecaptchaChallengeException()
        if possible_screens[match] == "only_once_a_minute_ready.pkl":
            print("Ready to submit rate-limited entry")
            # time.sleep(60)
            MouseReplayer("saved_mouse_movements/submit_rate_limited_entry.pkl")
            return
            # raise ScreenDoesNotMatchException()
        if possible_screens[match] == "Happy_reCAPTCHA_solved.pkl":
            MouseReplayer("saved_mouse_movements/submit_entry.pkl")
            return

        print("This should be unreachable")
        raise LogicError()

    def run_once(self):
        MouseReplayer("saved_mouse_movements/full.pkl")
        # MouseReplayer("saved_mouse_movements/first_click.pkl")
        # verify_screen_matches("saved_screen_captures/Happy_Info_Entry_Screen.pkl")
        # self.wait_and_verify("Happy_Info_Entry_Screennfo_Entry_Screen.pkl")
        # MouseReplayer("saved_mouse_movements/enter_name.pkl")
        # verify_screen_matches("saved_screen_captures/Happy_reCAPTCHA_solved.pkl")
        # self.check_recaptcha()
        # self.wait_and_verify("Happy_reCAPTCHA_solved.pkl")



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
