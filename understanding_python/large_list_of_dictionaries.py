import random


def get_dict():
    return {"a": random.random(),
            "b": random.random(),
            "c": random.random(),
            "d": "Some string"}


def get_list_of_dicts(n):
    return [get_dict() for _ in range(n)]


if __name__ == "__main__":
    d = get_list_of_dicts(100000)
