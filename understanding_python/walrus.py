import time


def walrus_while():
    start = time.time()
    then = start

    while (now := time.time()) - start < 5:
        dt = now - then
        print(f"The elsapsed time is {dt}")
        time.sleep(0.3)


class Foo:
    def __init__(self):
        self.bar = 0

    def set_and_return(self):
        pass
        # if self.bar := 1   # Cannot use walrus operator with attributes, only variables


def run_walrus_class():
    pass


if __name__ == "__main__":
    walrus_while()
