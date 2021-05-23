"""
Given a positive integer n, find the list of positive integers with sum n with maximal product

e.g. 6: [3, 3]: 3+3=6 and 3x3 = 9
"""
from functools import lru_cache


@lru_cache
def max_split(n):
    if n <= 4:
        return n

    return max_split(n - 3) * max_split(3)


def efficient_max_split(n):
    if n <= 4:
        return n

    num_threes = int(n / 3)
    rem = n - (3 * num_threes)
    if rem == 1:
        rem += 3
        num_threes -= 1
    if rem == 0:
        rem = 1
    return 3**num_threes * rem


if __name__ == "__main__":
    for i in range(1, 10):
        if max_split(i) != efficient_max_split(i):
            print(f"ERROR on {i}")
        print(f"{i}: {max_split(i)}")
    print(efficient_max_split(10000))
