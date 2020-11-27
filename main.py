# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy
import time
import math


def update_line(ax, hl, new_x_data, new_y_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_x_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_y_data))
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.001)


def plot_and_update():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plot, = ax.plot([], [])
    plt.pause(0.001)
    # x_data = range(10)
    # y_data = [x ** 2 for x in range(10)]
    # for x_datum, y_datum in zip(x_data, y_data):
    #     update_line(ax, plot, x_datum, y_datum)
    #     time.sleep(1)
    f = lambda x: math.sin(x ** 2)
    t0 = time.time()
    while time.time() - t0 < 10 and plt.fignum_exists(fig.number):
        t = time.time() - t0
        update_line(ax, plot, t, f(t))
        # time.sleep(0.01)


def plot_cont(fun, xmax):
    y = []
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    def update(i):
        yi = fun()
        y.append(yi)
        x = range(len(y))
        ax.clear()
        ax.plot(x, y)
        print(i, ': ', yi)

    a = anim.FuncAnimation(fig, update, frames=xmax, repeat=False)
    plt.show()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # plot_cont(lambda: 10, 10)
    plot_and_update()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
