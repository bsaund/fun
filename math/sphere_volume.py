from scipy.special import gamma
from matplotlib import pyplot as plt
from math import pi

Vs = []
R = 1
for n in range(1, 15):
    v = pi**(n/2) / gamma(n/2 + 1) * R**n

    cube_volume = (2*R)**n
    Vs.append(v/cube_volume)

plt.plot(Vs)
plt.xlabel('dimension')
plt.ylabel('Volume of R=1 Sphere / Vol of l=2 cube')
plt.yscale('log')
plt.show()
