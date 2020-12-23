

class Gripper:
    name = "hand"
    actions = None

    def __init__(self):
        self.actions = {"open": self.action_open,
                        "close": self.action_close}

    def action_open(self):
        print(f"Opening {self.name}")

    def action_close(self):
        print(f"Closing {self.name}")

