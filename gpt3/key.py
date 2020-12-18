
def get_secret_key(filename="~/.openai_key"):
    with open(filename) as f:
        return f.readline()
