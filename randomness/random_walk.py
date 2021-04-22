import numpy as np
from matplotlib import pyplot as plt

def random_walk():
    bounds = [10, 150]
    cur = np.random.randint(*bounds)
    num_samples = 10000

    values = [None]*num_samples
    for i in range(num_samples):
        cur += np.random.randint(-1, 2)
        if cur > bounds[1]:
            cur = bounds[1]
        if cur < bounds[0]:
            cur = bounds[0]
        # cur = np.clip(cur, *bounds)
        values[i] = cur

    plt.plot(values)
    plt.ylim(bounds)
    plt.show()


if __name__ == "__main__":
    random_walk()