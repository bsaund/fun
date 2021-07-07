from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import csv
from typing import List

bg_color = 'black'


class Topic(Enum):
    HISTORY = 'history'
    MATH = 'math'


@dataclass
class Flashcard:
    question: str
    answer: str
    short_name: str
    topic: Topic

    def to_dict(self):
        return {'short_name': self.short_name,
                'question': self.question,
                'answer': self.answer,
                'topic': self.topic,
                }


class Flashcards:
    def __init__(self, save_path='flashcards.csv'):
        self.cards: List[Flashcard] = []
        self.save_path = Path(save_path)
        self.load_flashcards()

    def load_flashcards(self):
        with self.save_path.open() as f:
            reader = csv.reader(f)

    def write_flashcards(self):
        if len(self.cards) == 0:
            raise RuntimeError("Cannot write empty list of cards")

        with self.save_path.open('w') as f:
            writer = csv.writer(f, delimiter=', ')
            header = list(self.cards[0].to_dict().keys())


class FlashcardDisplay:
    def __init__(self, parent):
        self.main_panel_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.add_item_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        parent.attributes("-fullscreen", True)
        # parent["bg"] = bg_color
        # self.canvas.pack()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.bind('<Escape>', self.quit)
        parent.bind('q', self.quit)

        self.make_main_panel_canvas()
        self.make_add_new_item_canvas()
        self.add_item_canvas.grid_remove()

    def make_main_panel_canvas(self):
        self.main_panel_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.main_panel_canvas.columnconfigure(0, weight=1)
        self.main_panel_canvas.rowconfigure(0, weight=1)

        new_item_button = tk.Button(self.main_panel_canvas, text="Add entry",
                                    command=self.switch_to_new_item_canvas)
        new_item_button.grid(column=0, row=0, sticky=tk.SE)

    def make_add_new_item_canvas(self):
        self.add_item_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.add_item_canvas.columnconfigure(0, weight=1)
        self.add_item_canvas.rowconfigure(0, weight=1)

        cancel = tk.Button(self.add_item_canvas, text="Cancel",
                           command=self.switch_to_main_canvas)
        cancel.grid(column=0, row=0, sticky=tk.SE)

    def switch_to_new_item_canvas(self):
        self.main_panel_canvas.grid_remove()
        self.add_item_canvas.grid()
        print("Adding a new item")

    def switch_to_main_canvas(self):
        self.add_item_canvas.grid_remove()
        self.main_panel_canvas.grid()
        print("Switching to main canvas")

    def quit(self, _event=None):
        print("Calling it quits")
        self.main_panel_canvas.quit()
        self.main_panel_canvas.destroy()


if __name__ == "__main__":
    # s = ttk.Style()
    root = tk.Tk()
    print(f'themes: {ttk.Style().theme_names()}')
    print(ttk.Style().theme_use())
    # s = ttk.Style()
    # s.theme_use('clam')
    root.style = ttk.Style()
    root.style.theme_use("clam")
    root.wm_title = ("Flashcards")
    FlashcardDisplay(root)
    root.mainloop()
