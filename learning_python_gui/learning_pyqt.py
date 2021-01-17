from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class LabeledSlider(QtWidgets.QWidget):
    def __init__(self, name, maximum=1.0, minimum=0.0, initial_value=1.0, tickInterval=1.0):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()

        self.name = name
        self.label = QtWidgets.QLabel(f"{name}: 0", self)

        self.scale = 1.0 / tickInterval
        self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(int(np.floor(minimum * self.scale)))
        self.slider.setMaximum(int(np.ceil(maximum * self.scale)))
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_label)
        self.slider.setValue(int(initial_value * self.scale))

        layout.addWidget(self.label)
        layout.addSpacing(10)
        layout.addWidget(self.slider)
        self.setLayout(layout)
        self.update_label()

    def update_label(self):
        self.label.setText(f"{self.name}: {self.value()}")

    def value(self):
        return self.slider.value() / self.scale


class InteractiveSin(QtWidgets.QTabWidget):
    a = 1
    w = 1
    plot_ref = None

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        title = QtWidgets.QLabel("Here is a graph of a*sin(w*t)", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.plot_canvas = MplCanvas(parent=self, width=5, height=4, dpi=100)
        self.redraw()
        layout.addWidget(self.plot_canvas)

        self.a_slider = LabeledSlider(name="A", maximum=1.0, minimum=0.0, tickInterval=0.01)
        self.a_slider.slider.valueChanged.connect(self.on_a_slider_change)
        layout.addWidget(self.a_slider)

        self.w_slider = LabeledSlider(name="w", maximum=5.0, minimum=0.2, tickInterval=0.01)
        self.w_slider.slider.valueChanged.connect(self.on_w_slider_change)
        layout.addWidget(self.w_slider)

        self.setLayout(layout)

    def redraw(self):
        t = np.arange(0, 10, 0.01)
        y = self.a * np.sin(self.w * t * np.pi)

        if self.plot_ref is None:
            self.plot_ref = self.plot_canvas.axes.plot(t, y)[0]

        self.plot_ref.set_ydata(y)
        self.plot_canvas.draw()

    def on_a_slider_change(self):
        self.a = self.a_slider.value()
        self.redraw()

    def on_w_slider_change(self):
        self.w = self.w_slider.value()
        self.redraw()


class InteractiveLine(QtWidgets.QTabWidget):
    m = 1
    b = 0
    plot_ref = None

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()

        title = QtWidgets.QLabel("And here is mx + b", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.plot_canvas = MplCanvas(parent=self, width=5, height=4, dpi=100)
        self.redraw()
        layout.addWidget(self.plot_canvas)

        self.m_slider = LabeledSlider(name="m", maximum=1.0, minimum=0.0, tickInterval=0.01)
        self.m_slider.slider.valueChanged.connect(self.on_m_slider_change)
        layout.addWidget(self.m_slider)

        self.b_slider = LabeledSlider(name="b", maximum=5.0, minimum=-5.0, tickInterval=0.01, initial_value=self.b)
        self.b_slider.slider.valueChanged.connect(self.on_b_slider_change)
        layout.addWidget(self.b_slider)

        self.setLayout(layout)

    def redraw(self):
        t = np.arange(0, 10, 0.01)
        y = self.m * t + self.b

        if self.plot_ref is None:
            self.plot_ref = self.plot_canvas.axes.plot(t, y)[0]

        self.plot_ref.set_ydata(y)
        self.plot_canvas.draw()

    def on_m_slider_change(self):
        self.m = self.m_slider.value()
        self.redraw()

    def on_b_slider_change(self):
        self.b = self.b_slider.value()
        self.redraw()


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        # sc = InteractiveSin()

        layout.addWidget(InteractiveSin(), 0, 0)
        layout.addWidget(InteractiveLine(), 1, 0)

        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setCentralWidget(MainWidget())
        self.show()
        self.resize(1000, 1000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
