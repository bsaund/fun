class Arm:
    name = "arm"
    actions = None

    def __init__(self):
        self.actions = {"move": self.move}

    def move(self):
        print(f"Moving {self.name}")
