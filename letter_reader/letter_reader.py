import pynput
import os
import signal
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess


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
}


def gen_filepath(speech):
    return os.path.join("./letter_mp3s", f"{speech}.mp3")


class LetterReader:
    def __init__(self):
        try:
            self.polly = boto3.Session(profile_name="adminuser").client("polly")
        except:
            self.polly = None
            print("Warning - unable to connect to AWS. Unable to get new letters")

        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        self.letter_to_speak = None
        self.should_exit = False


    def run(self):
        while not self.should_exit:
            if self.letter_to_speak is not None:
                self.speak(self.letter_to_speak)
                self.letter_to_speak = None
        print("Exiting")
        return


    def on_press(self, key):
        if key == pynput.keyboard.Key.esc:
            self.should_exit = True
            print("Esc Pressed")
            return
        self.letter_to_speak = key

    def generate_new_mp3(self, speech):
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
            output = gen_filepath(speech)

            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())

    def speak(self, key):
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

        if not os.path.exists(gen_filepath(char)):
            self.generate_new_mp3(char)
        fp = gen_filepath(char)
        print(f"Opening file {fp}")
        subprocess.Popen(['mpg123', '-q', '--no-control', fp]).wait()


if __name__ == "__main__":
    print(HELP_STR)
    lr = LetterReader()
    # lr.generate_new_mp3("a")
    lr.run()
