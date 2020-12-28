public1 = 12232269
public2 = 19452773

# tmp
# public1 = 5764801
# public2 = 17807724

divisor = 20201227


def determine_loop_size(public_key, subject=7, max_check=100000000):
    val = 1
    for i in range(1, max_check):
        val = val * subject % divisor
        if val == public_key:
            return i
    raise Exception(f"loop size is greater than {max_check}")


def transform(loop_size, subject=7):
    val = 1
    for _ in range(loop_size):
        val = val * subject % divisor
    return val


ls1 = determine_loop_size(public1)
ls2 = determine_loop_size(public2)

print(f"{ls1=}, {ls2=}")
print(transform(subject=public1, loop_size=ls2))
print(transform(subject=public2, loop_size=ls1))
