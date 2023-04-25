import pynput
import os
import signal
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess
import argparse
import time

HELP_STR = '''
Welcome to Letter Presser
Press any letter to have a voice read it.
Press esc to exit
'''

SPECIAL_KEY_MAP = {
    pynput.keyboard.Key.backspace: "Backspace",
    pynput.keyboard.Key.delete: "Delete",
    pynput.keyboard.KeyCode.from_char('/'): "slash",
    pynput.keyboard.KeyCode.from_char('*'): "asterix",
    pynput.keyboard.Key.left: "left",
    pynput.keyboard.Key.right: "right",
    pynput.keyboard.Key.up: "up",
    pynput.keyboard.Key.down: "down",
    pynput.keyboard.Key.tab: "Tab",
    pynput.keyboard.Key.caps_lock: "Caps Lock",
    pynput.keyboard.KeyCode.from_char(','): "comma",
    pynput.keyboard.Key.shift: "shift",
    pynput.keyboard.Key.shift_r: "shift",
    pynput.keyboard.Key.space: "space"
}


def gen_filepath(speech):
    return os.path.join("./letter_mp3s", f"{speech}.mp3")


def gen_word_filepath(speech):
    return os.path.join("./word_mp3s", f"{speech}.mp3")


class LetterReader:
    def __init__(self, read_words=False):
        try:
            self.polly = boto3.Session(profile_name="adminuser").client("polly")
        except:
            print("Warning - unable to connect to AWS. Unable to get new letters")

        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.letter_to_speak = None
        self.should_exit = False
        self.read_words = read_words
        print(self.read_words)
        self.word_buffer = []
        self.last_update_time = time.time()

    def run(self):
        while not self.should_exit:
            if self.letter_to_speak is not None:
                self.word_buffer.append(self.letter_to_speak)
                self.speak_letter(self.letter_to_speak)
                self.last_update_time = time.time()
                self.letter_to_speak = None
            if self.read_words \
                    and len(self.word_buffer) > 0 \
                    and time.time() - self.last_update_time > 3:
                self.speak_word(self.word_buffer)
                self.word_buffer = []

        print("Exiting")
        return

    def on_press(self, key):
        if key == pynput.keyboard.Key.esc:
            self.should_exit = True
            print("Esc Pressed")
            return
        self.letter_to_speak = key

    def generate_new_mp3(self, speech, filepath):
        if self.polly is None:
            return

        print(f"Generating new mp3 for {speech}")
        try:
            response = self.polly.synthesize_speech(Text=speech, OutputFormat="mp3", VoiceId="Matthew")
        except (BotoCoreError, ClientError) as error:
            raise error

        if "AudioStream" not in response:
            raise Exception("AudioStream not found")

        with closing(response["AudioStream"]) as stream:
            # output = gen_filepath(speech)

            # Open a file for writing the output as a binary stream
            with open(filepath, "wb") as file:
                file.write(stream.read())

    def speak_letter(self, key):
        print(f"Speaking {key}")
        if key == pynput.keyboard.Key.esc:
            print("Raising exception")
            os.kill(os.getpid(), signal.SIGUSR1)

        if key in SPECIAL_KEY_MAP:
            char = SPECIAL_KEY_MAP[key]
        else:
            try:
                char = key.char
            except AttributeError:
                print("Exception!")
                return
        fp = gen_filepath(char)
        if not os.path.exists(gen_filepath(char)):
            self.generate_new_mp3(char, fp)

        print(f"Opening file {fp}")
        subprocess.Popen(['mpg123', '-q', '--no-control', fp]).wait()

    def speak_word(self, key_array: list):
        print(f"Speaking {key_array}")

        letter_array = [k.char for k in key_array]

        word = "".join(letter_array)
        print(word)
        fp = gen_word_filepath(word)
        self.generate_new_mp3(word, fp)
        print(f"Opening file {fp}")
        subprocess.Popen(['mpg123', '-q', '--no-control', fp]).wait()

def get_parser():
    parser = argparse.ArgumentParser(
        prog='Letter Reader',
        description='Reads letters when pressed. A good toy for kids'
    )
    parser.add_argument('--read_words', action='store_true', help='Read the word after the individual letters')
    return parser


if __name__ == "__main__":
    print(HELP_STR)
    args = get_parser().parse_args()
    print(args)
    lr = LetterReader(args.read_words)
    # lr.generate_new_mp3("a")
    lr.run()
