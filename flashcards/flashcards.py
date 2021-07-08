from dataclasses import dataclass
from enum import Enum
import tkinter as tk
import random
from tkinter import ttk
from pathlib import Path
import csv
from typing import List, Optional
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
        self.flashcard_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.add_item_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        self.entry_panel = None
        self.flashcard_panel = None
        self.flashcards = flashcards
        parent.attributes("-fullscreen", True)
        # parent["bg"] = bg_color
        # self.canvas.pack()
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.bind('<Escape>', self.quit)
        quit_button = tk.Button(parent, text="Quit", command=self.quit)
        quit_button.grid(sticky=tk.SW)
        # parent.bind('q', self.quit)

        self.make_main_panel_canvas()
        self.make_add_new_item_canvas()
        self.add_item_canvas.grid_remove()

        if len(self.flashcards.cards) == 0:
            self.switch_to_new_item_canvas()

    def make_main_panel_canvas(self):
        self.flashcard_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.flashcard_canvas.columnconfigure(0, weight=1)
        self.flashcard_canvas.rowconfigure(0, weight=1)
        new_item_button = tk.Button(self.flashcard_canvas, text="Add entry",
                                    command=self.switch_to_new_item_canvas)
        new_item_button.grid(column=0, row=0, sticky=tk.SE)
        self.flashcard_panel = FlashCardPanel(self.flashcard_canvas, self.flashcards)

    def make_add_new_item_canvas(self):
        self.add_item_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.add_item_canvas.columnconfigure(0, weight=1)
        self.add_item_canvas.rowconfigure(0, weight=1)
        self.entry_panel = EntryPanel(self.add_item_canvas, self.add_new_entry_callback)

        if len(self.flashcards.cards) == 0:
            self.entry_panel.header = tk.Label(self.add_item_canvas, text="You Currently have No Flashcards")
            self.entry_panel.header.grid(column=0, row=0, sticky=tk.N, pady=20)

        cancel = tk.Button(self.add_item_canvas, text="Flashcards",
                           command=self.switch_to_main_canvas)
        cancel.grid(column=0, row=0, sticky=tk.SE)

    def add_new_entry_callback(self):
        entry = self.entry_panel.get()
        if entry is None:
            return

        fc = Flashcard(**entry)
        self.flashcards.cards.append(fc)
        self.flashcards.write_flashcards()

        if self.entry_panel.header is not None:
            self.entry_panel.header.grid_forget()

        self.entry_panel.clear_user_input()
        print("Adding new entry")

    def switch_to_new_item_canvas(self):
        self.flashcard_canvas.grid_remove()
        self.add_item_canvas.grid()
        print("Adding a new item")

    def switch_to_main_canvas(self):
        self.add_item_canvas.grid_remove()
        self.flashcard_canvas.grid()
        print("Switching to main canvas")

    def quit(self, _event=None):
        print("Calling it quits")
        self.flashcard_canvas.quit()
        self.flashcard_canvas.destroy()


class FlashCardPanel:
    def __init__(self, parent, flashcards: Flashcards, main_column_width=500, side_column_width=200):
        self.canvas = tk.Canvas(parent, bd=2, relief='ridge')
        self.canvas.grid(row=0, column=0)
        self.canvas.columnconfigure(1, minsize=main_column_width)
        self.canvas.columnconfigure(0, minsize=side_column_width)
        self.canvas.columnconfigure(2, minsize=side_column_width)
        self.flashcards = flashcards
        self.active_card: Optional[Flashcard] = None
        random.shuffle(self.flashcards.cards)
        self.cards_iter = self.flashcards.cards.__iter__()

        self.topic_label = tk.Label(self.canvas)
        self.topic_label.grid(column=0, row=0, padx=10, pady=10)

        self.short_name_label = tk.Label(self.canvas)
        self.short_name_label.grid(column=2, row=0, padx=10, pady=10)

        self.canvas.rowconfigure(1, minsize=50)

        self.question_label = tk.Message(self.canvas, width=main_column_width - 10)
        self.question_label.grid(column=1, row=2)
        self.canvas.rowconfigure(2, minsize=200)

        self.canvas.rowconfigure(3, minsize=50)

        self.answer_label = tk.Message(self.canvas, width=main_column_width - 10)
        self.answer_label.grid(column=1, row=4)
        self.canvas.rowconfigure(4, minsize=200)

        self.reveal_answer_button = tk.Button(self.canvas, command=self.reveal_answer, text="Reveal Answer")
        self.reveal_answer_button.grid(column=1, row=10, sticky=tk.S, pady=30)

        self.next_card_button = tk.Button(self.canvas, command=self.get_next_card, text="Next Card")
        self.next_card_button.grid(column=1, row=10, sticky=tk.S, pady=30)

        self.get_next_card()

    def get_next_card(self):
        try:
            self.active_card = next(self.cards_iter)
        except StopIteration:
            print(f"{Fore.RED}Final flashcard reached{Fore.RESET}")

        self.topic_label.config(text=f"Topic: {self.active_card.topic}")
        self.short_name_label.config(text=f"{self.active_card.short_name}")
        self.question_label.config(text=f"{self.active_card.question}")
        self.answer_label.config(text=f"{self.active_card.answer}")
        self.answer_label.grid_remove()

        self.next_card_button.grid_remove()
        self.reveal_answer_button.grid()

    def reveal_answer(self):
        print("Revealing answer")
        self.next_card_button.grid()
        self.reveal_answer_button.grid_remove()
        self.answer_label.grid()


class EntryPanel:
    def __init__(self, parent, callback, size=30):
        entry_canvas = tk.Canvas(parent)
        entry_canvas.grid(row=0, column=0)
        self.header = None

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
