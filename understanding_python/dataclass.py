from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class MyData:
    name: str
    min_val: int
    max_val: float


if __name__ == "__main__":
    data1 = MyData(name='data1', min_val=1, max_val=1.5)
    print(data1)
    data2 = MyData(name='data2', min_val=1.5, max_val=2.5)
    print(data2)
    print(data1)

    mapping = {data1: "data1", data2: "data2"}
    print(mapping.keys())
