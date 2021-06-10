import numpy as np
import scipy.stats

"""
I am curious about sampling variance of very unlikely events, such as successfully farming a chia
"""


def sample_expected_one(n: int):
    return np.sum(np.random.rand(n) < 1 / n)


def simulate(num_samples, num_trials=10000):
    num_wins = [sample_expected_one(num_samples) for _ in range(num_trials)]
    return num_wins


def stats(num_samples, num_trials=10000):
    num_wins = simulate(num_samples, num_trials)
    print(f"Using {num_samples} samples, the mean is {np.mean(num_wins)} with variance {np.var(num_wins)}")


def chance_of_no_win(num_samples, num_trials=10000):
    wins = simulate(num_samples, num_trials)
    num_zeros = len(wins) - np.count_nonzero(wins)
    print(f"Chance of not winning {num_zeros / len(wins)}")
    scipy.stats.norm.pdf(1)


def analytic(n: int):
    chance_no_win = ((n-1)/n)**n
    print(f"Analytically, the chance of not winning with {n=} is {chance_no_win}")



def main():
    for num_samples in [2, 10, 100, 1000, 10000]:
        stats(num_samples)
        chance_of_no_win(num_samples)
        analytic(num_samples)
    analytic(n=1000000)



if __name__ == "__main__":
    main()
