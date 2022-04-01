import pyautogui
import pynput
from utils.timestamp import timestamp
import cv2
import time
from PIL import Image
import pickle


class ScreenCapture:
    def __init__(self):
        file_base = f"screen_captures/capture_{timestamp()}"
        fn = f"{file_base}.pkl"
        img = pyautogui.screenshot()

        self.upper_left = None
        self.lower_right = None

        print("Click upper left corner")
        with pynput.mouse.Listener(on_click=self.set_upper_left) as listener:
            listener.join()

        # time.sleep(1)

        print("Click lower right corner")
        with pynput.mouse.Listener(on_click=self.set_lower_right) as listener:
            listener.join()

        # img = Image.open(fn)
        img = img.crop(self.upper_left + self.lower_right)
        # img.save(fn)
        with open(fn, "wb+") as f:
            obj = {"image": img,
                   "upper_left": self.upper_left,
                   "lower_right": self.lower_right}
            pickle.dump(obj, f)

        print(f"Saved image as {fn}")

    def set_upper_left(self, x, y, button, pressed):
        if pressed == False:
            return True
        self.upper_left = (x, y)
        return False

    def set_lower_right(self, x, y, button, pressed):
        if pressed == False:
            return True
        self.lower_right = (x, y)
        return False


class ScreenVerify:
    def __init__(self, fn):
        with open(fn, "rb") as f:
            self.data = pickle.load(f)

    def matches(self):
        img = pyautogui.screenshot()
        img = img.crop(self.data['upper_left'] + self.data['lower_right'])

        if img == self.data['image']:
            print("Matches")
        else:
            print("does not match")


class ScreenDoesNotMatchException(Exception):
    pass


def screen_matches(fn):
    with open(fn, "rb") as f:
        data = pickle.load(f)
    img = pyautogui.screenshot()
    img = img.crop(data['upper_left'] + data['lower_right'])

    if img == data['image']:
        # print("Matches")
        return True
    else:
        # print("does not match")
        return False


def verify_screen_matches(fn):
    if not screen_matches(fn):
        print(f"Screen does not match for {fn}")
        raise ScreenDoesNotMatchException()


if __name__ == "__main__":
    ScreenCapture()
    # ScreenVerify("screen_captures/capture_2022_03_30-21_00_46.pkl").matches()
    # fn = "saved_screen_captures/expected_entry_screen.pkl"
    # screen_matches(fn)
