from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
import numpy as np


class ScatterPlot(FigureCanvas):
    marker_size = 1
    marker_format = 'k.'

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.initial_xlim = None
        self.initial_ylim = None

        self.clear()

    def plot(self, x_list=None, y_list=None, marker_format=None, marker_size=None):
        if x_list is None or y_list is None:
            raise TypeError('Must pass two data lists')

        if marker_format is None:
            marker_format = self.marker_format
        if marker_size is None:
            marker_size = self.marker_size

        self.axes.plot(x_list, y_list, marker_format,
                       markersize=marker_size)

        self.save_initial_lim()
        self.reflow()
        self.draw()

    def save_initial_lim(self):
        self.initial_xlim = self.axes.get_xlim()
        self.initial_ylim = self.axes.get_ylim()

    def plot_random(self):
        x_list, y_list = np.random.randn(2, 100)
        self.plot(x_list, y_list)

    def clear(self):
        self.axes.clear()
        self.axes.grid()
        self.draw()

    def reflow(self):

        height = self.figure.get_figheight()
        width = self.figure.get_figwidth()
        x_to_y_ratio = width/height

        xlim = self.initial_xlim
        ylim = self.initial_ylim

        if None in(xlim, ylim):
            return

        half_max_axis_range = max((xlim[1]-xlim[0]),
                                  ylim[1]-ylim[0])/2

        x_shift_factor, y_shift_factor = half_max_axis_range, half_max_axis_range

        if x_to_y_ratio > 1:  # Landscape mode
            x_shift_factor = half_max_axis_range*x_to_y_ratio

        elif x_to_y_ratio < 1:  # Portrait mode
            y_shift_factor = half_max_axis_range/x_to_y_ratio

        new_xlim = [np.average(xlim) - x_shift_factor,
                    np.average(xlim) + x_shift_factor]
        new_ylim = [np.average(ylim) - y_shift_factor,
                    np.average(ylim) + y_shift_factor]

        self.axes.set_xlim(new_xlim)
        self.axes.set_ylim(new_ylim)
