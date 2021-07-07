from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import csv
from typing import List
from colorama import Fore

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
        self.delimiter = '\t'
        self.cards: List[Flashcard] = []
        self.save_path = Path(save_path)
        self.load_flashcards()


    def load_flashcards(self):
        if not self.save_path.exists():
            print(f"{Fore.RED}No existing flashcards found{Fore.RESET}")
            return
        with self.save_path.open() as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            header = next(reader, None)
            for row in reader:
                d = {k: v for k, v in zip(header, row)}
                self.cards.append(Flashcard(**d))

    def write_flashcards(self):
        if len(self.cards) == 0:
            raise RuntimeError("Cannot write empty list of cards")

        with self.save_path.open('w') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            header = list(self.cards[0].to_dict().keys())
            writer.writerow(header)
            for card in self.cards:
                writer.writerow([card.to_dict()[k] for k in header])


class FlashcardDisplay:
    def __init__(self, parent, flashcards):
        self.main_panel_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.add_item_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.entry_canvas = None
        self.flashcards = flashcards
        parent.attributes("-fullscreen", True)
        # parent["bg"] = bg_color
        # self.canvas.pack()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.bind('<Escape>', self.quit)
        # parent.bind('q', self.quit)

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
        self.entry_canvas = EntryGrid(self.add_item_canvas, self.add_new_entry_callback)

        cancel = tk.Button(self.add_item_canvas, text="Cancel",
                           command=self.switch_to_main_canvas)
        cancel.grid(column=0, row=0, sticky=tk.SE)

    def add_new_entry_callback(self):
        entry = self.entry_canvas.get()
        if entry is None:
            return

        fc = Flashcard(**entry)
        self.flashcards.cards.append(fc)
        self.flashcards.write_flashcards()

        self.entry_canvas.clear_user_input()
        print("Adding new entry")

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


class EntryGrid:
    def __init__(self, parent, callback, size=30):
        entry_canvas = tk.Canvas(parent)
        entry_canvas.grid(row=0, column=0)

        l1 = tk.Label(entry_canvas, text="short name")
        l1.config(font=(None, size))
        self.short_name_entry = tk.Entry(entry_canvas, width=30, font=(None, size))
        l1.grid(row=0, column=0)
        self.short_name_entry.grid(row=0, column=1)

        ltopic = tk.Label(entry_canvas, text="topic", font=(None, size))
        ltopic.grid(row=1, column=0)
        self.topic_entry = tk.Entry(entry_canvas, width=30, font=(None, size))
        self.topic_entry.grid(row=1, column=1)

        l2 = tk.Label(entry_canvas, text="question", font=(None, size))
        l2.grid(row=2, column=0)
        self.question_entry = tk.Entry(entry_canvas, width=100)
        self.question_entry.grid(row=2, column=1)

        l3 = tk.Label(entry_canvas, text="answer")
        l3.grid(row=3, column=0)
        l3.config(font=(None, size))
        self.answer_entry = tk.Entry(entry_canvas, width=100)
        self.answer_entry.grid(row=3, column=1)

        b = tk.Button(entry_canvas, text="Submit", command=callback)
        b.grid(row=4, column=0, columnspan=2)

    def get(self, validate=True):
        short_name = self.short_name_entry.get()
        question = self.question_entry.get()
        answer = self.answer_entry.get()
        topic = self.topic_entry.get()

        if validate:
            valid = True
            if len(short_name) == 0:
                valid = False
                print("Need to include a shortname")
            if len(question) == 0:
                valid = False
                print("Need to include a question")
            if len(answer) == 0:
                valid = False
                print("Need to include an answer")

            if len(topic) == 0:
                valid = False
                print("Need to include an topic")
            if not valid:
                return None

        return {"short_name": short_name, "question": question, "answer": answer, "topic": topic}

    def clear_user_input(self):
        print("Clearing text")
        self.short_name_entry.delete(0, 'end')
        self.question_entry.delete(0, 'end')
        self.answer_entry.delete(0, 'end')
        self.topic_entry.delete(0, 'end')




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
    FlashcardDisplay(root, Flashcards())
    root.mainloop()
