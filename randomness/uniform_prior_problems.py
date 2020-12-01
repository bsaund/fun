import matplotlib.pyplot as plt
import random


def flip(bias):
    return int(random.random() > bias)


def sample_bias():
    # return random.random()
    return random.random()**2


results = [0, 0]
for i in range(1000):
    bias = sample_bias()
    results[flip(bias)] += 1

plt.bar(['heads', 'tails'], results)
plt.show()
