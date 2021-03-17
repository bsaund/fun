from functools import lru_cache
import time

FIB_CACHE_CALLS = 0
FIB_NO_CACHE_CALLS = 0
FIB_BUILD_CALLS = 0


@lru_cache
def fib_cache(n):
    global FIB_CACHE_CALLS
    FIB_CACHE_CALLS += 1
    if n in [1, 2]:
        return 1
    return fib_cache(n - 1) + fib_cache(n - 2)


def fib_no_cache(n):
    global FIB_NO_CACHE_CALLS
    FIB_NO_CACHE_CALLS += 1
    if n in [1, 2]:
        return 1
    return fib_no_cache(n - 1) + fib_no_cache(n - 2)


def fib_build_calls(n):
    global FIB_BUILD_CALLS
    if n in [1, 2]:
        return 1
    l1 = 1
    l2 = 1
    for i in range(n-2):
        FIB_BUILD_CALLS += 1
        tmp = l1 + l2
        l1 = l2
        l2 = tmp
        # print(l2)
    return l2


if __name__ == "__main__":
    num = 100
    # print(fib_cache(num))
    # print(fib_no_cache(num))
    print(fib_build_calls(num))

    print(f'{FIB_CACHE_CALLS=}')
    # print(f'{FIB_NO_CACHE_CALLS=}')
    print(f'{FIB_BUILD_CALLS=}')
