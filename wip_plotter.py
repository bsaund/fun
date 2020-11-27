from plotter import TimeSeriesPlotter
import time
import math


def main():
    tsp = TimeSeriesPlotter(['all', 'b'])

    f = lambda x: math.sin(x ** 2)
    t0 = time.time()
    while time.time() - t0 < 100 and tsp.is_open():
        t = time.time() - t0
        # new_data = {'all': t + t ** 2/5,
        #             'b': math.sin(t) ** 2}
        new_data = {'all': math.sin(t)}
        if t % 1 < 0.5:
            new_data['b'] = math.sin(t)
        tsp.update(t, new_data)
        # time.sleep(0.01)


if __name__ == "__main__":
    main()
