import abc


class Parent(abc.ABC):
    def __init__(self, data):
        self.data = data

    def make_copy_from_subselection(self, lower, upper):
        return self.__class__(self.data[lower: upper])


class Child(Parent):
    def __init__(self, data):
        super().__init__(data)

    def print(self):
        print(f"This is the child class, reporting {self.data}")


if __name__ == "__main__":
    child = Child([1, 2, 3, 4, 5])
    child.print()
    child2 = child.make_copy_from_subselection(1, 3)
    child2.print()
    print("The child made a copy using the child class. Success!")
