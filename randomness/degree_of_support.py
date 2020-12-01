
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

def f(x):
    return max(2 * x - 1, 0)


x = [i for i in np.linspace(0, 1, 21)]
y = [f(a) for a in x]
print(x)

plt.plot(x, y)
plt.xlabel("$h(x_q)$", fontsize=40)
plt.ylabel("$\pi(+1 | h, x_q)$", fontsize=40)
plt.show()
