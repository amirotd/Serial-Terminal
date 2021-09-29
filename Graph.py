from PyQt5 import QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg
import sys


class MyPlotWindow:

    def __init__(self):
        self.data = [0]
        self.traces = dict()
        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)
        self.cnt = 0

        pg.setConfigOptions(antialias=True)
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title="Basic plotting example")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyQtGraph example : plotting')
        self.canvas = self.win.addPlot(title='Serial Data')
        self.canvas.showGrid(x=True, y=True, alpha=0.5)
        self.canvas.setLabel('left', 'amplitude', units='y')
        self.canvas.setLabel('bottom', 'Time', units='s')

        self.traces = self.canvas.plot(pen='y')

    @staticmethod
    def start():
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()

    def trace(self, dataset_y):
        self.traces.setData(dataset_y)
        self.canvas.setXRange(self.cnt - 200, self.cnt + 5, padding=0)

    def animation(self, serdata):
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: self.update(serdata))
        timer.start()
        self.start()

    def update(self, inputdata):
        # s = np.sin(2 * np.pi * self.t + self.phase)
        # self.trace(self.t, s)
        # self.phase += 0.1
        self.data.append(inputdata)
        xdata = np.array(self.data, dtype='float64')
        self.trace(xdata)
        self.app.processEvents()

        self.cnt = self.cnt + 1


if __name__ == '__main__':
    p = MyPlotWindow()
    p.animation(2)
