from functools import lru_cache


class A:
    def __init__(self):
        self.foo = 1

    @lru_cache()
    def add_to_foo(self, bar):
        print("Running non-cached version of add_to_foo")
        return self.foo + bar


if __name__ == "__main__":
    a = A()
    print(a.add_to_foo(1))
    print(a.add_to_foo(1))
    print(a.add_to_foo(2))
    a.foo = 0
    print(a.add_to_foo(1))  # THIS DOES NOT UPDATE USING THE NEW MEMBER VARIABLE
    print(a.add_to_foo(3))  # since this was not cached, the output is as expected
