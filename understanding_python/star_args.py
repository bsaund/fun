

def my_fun(*some_args, kwarg=True):
    for a in some_args:
        print(f"args {a}")
    print(kwarg)


if __name__ == "__main__":
    my_fun("a", "b", "c")
    my_fun("a", "b", "c", False)
