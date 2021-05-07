import numpy as np

int_max = np.array([2**32-1])
int32_max = (int_max).astype(np.uint32)

float32 = int_max.astype(np.float32)
back_to_int32 = float32.astype(np.int32)

print(int_max)
print(int32_max)
print(float32)
print(back_to_int32)

