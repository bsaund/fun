import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import typing


class TimeSeriesPlotter:
    def __init__(self, fields, min_time=10, max_time_interval=10):
        self.fields = fields
        self.fig = plt.figure()
        self.axes = {field: self.fig.add_subplot(len(fields), 1, i + 1) for i, field in enumerate(fields)}
        self.plots = {field: self.axes[field].plot([], [])[0] for field in fields}
        self.min_time = min_time
        self.max_time_interval = max_time_interval

        for field in fields:
            self.axes[field].set_title(field)
        plt.tight_layout()
        plt.pause(0.001)

    def is_open(self):
        return plt.fignum_exists(self.fig.number)

    def update(self, x, y_dict: typing.Dict[str, float]):
        for field, y in y_dict.items():
            hl = self.plots[field]
            hl.set_xdata(np.append(hl.get_xdata(), x))
            y_data = np.append(hl.get_ydata(), y)
            hl.set_ydata(y_data)
            self.axes[field].relim()
            border = (max(y_data) - min(y_data)) * 0.05
            self.axes[field].set_ylim([min(y_data) - border, max(y_data) + border])
            # self.axes[field].set_xlim([0, x])
            # self.axes[field].au
        for field, ax in self.axes.items():
            ax.set_xlim([max(0, x - self.max_time_interval), max(x, self.min_time)])
        plt.draw()
        plt.pause(0.001)
