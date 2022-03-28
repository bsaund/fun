import pyautogui
import pynput
from utils.timestamp import timestamp
import cv2
import PIL


class ScreenCapture:
    def __init__(self):
        fn = f"screen_captures/capture_{timestamp()}.png"
        img = pyautogui.screenshot()

        self.upper_left = None
        self.lower_right = None

        print("Click upper left corner")
        with pynput.mouse.Listener(on_click=self.set_upper_left) as listener:
            listener.join()

        print("Click lower right corner")
        with pynput.mouse.Listener(on_click=self.set_lower_right) as listener:
            listener.join()



        print(f"Saved image as {fn}")


    def set_upper_left(self, x, y, button, pressed):
        self.upper_left = (x, y)
        return False


    def set_lower_right(self, x, y, button, pressed):
        self.lower_right = (x, y)
        return False


if __name__ == "__main__":
    ScreenCapture()
