class Foo:
    def __init__(self, val):
        self.val = 1

    def __add__(self, other):
        self.val += other


def add_one(var):
    var += 1
    return var


def append_50(lst):
    lst += (50,)


def test_assignment(foo):
    foo = 2


def test_adding_one():
    a = 1
    add_one(a)
    assert a == 1

    foo = Foo(1)
    add_one(foo)
    assert foo.val == 2

    a = [1, 2, 3]
    append_50(a)
    assert len(a) == 4

    b = (1, 2, 3)
    append_50(b)
    assert len(b) == 3

    a = 1
    test_assignment(a)
    assert a == 1


if __name__ == "__main__":
    test_adding_one()
