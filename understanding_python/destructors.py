

class Foo:
    def __init__(self):
        print('init called')

    def __del__(self):
        print('del called')


def main():
    foo = Foo()
    print("middle of the function")
    del foo
    print("foo should already have been deleted")


if __name__ == "__main__":
    main()