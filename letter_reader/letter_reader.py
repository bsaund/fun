import pynput
import os
import signal
import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import subprocess


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

    def run(self):
        while self.letter_to_speak != 'esc':
            if self.letter_to_speak is not None:
                self.speak(self.letter_to_speak)
                self.letter_to_speak = None
        print("Exiting")

    def on_press(self, key):
        self.letter_to_speak = key
        print(f"set letter to speak as {key}")

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
        if key == pynput.keyboard.Key.esc:
            print("Raising exception")
            os.kill(os.getpid(), signal.SIGUSR1)

        try:
            key.char
        except AttributeError:
            return

        if not os.path.exists(gen_filepath(key.char)):
            self.generate_new_mp3(key.char)

        subprocess.Popen(['mpg123', '-q', gen_filepath(key.char)]).wait()


if __name__ == "__main__":
    lr = LetterReader()
    # lr.generate_new_mp3("a")
    lr.run()