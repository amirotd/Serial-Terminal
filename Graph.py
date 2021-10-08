from PyQt5 import QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg
import sys


class MyPlotWindow:

    def __init__(self):
        self._data = [0]
        self._cnt = 0

        pg.setConfigOptions(antialias=True)
        self._app = QtWidgets.QApplication(sys.argv)
        self._win = pg.GraphicsWindow(title="Plotting Window")
        self._win.resize(1000, 600)
        self._win.setWindowTitle('Serial Data : plotting')
        self._win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.CustomizeWindowHint)
        self._win.show()
        self._canvas = self._win.addPlot(title='Serial Data')
        self._canvas.showGrid(x=True, y=True, alpha=0.5)
        self._canvas.setLabel('left', 'amplitude')
        self._canvas.setLabel('bottom', 'Time')
        self._traces = self._canvas.plot(pen='y')

    @staticmethod
    def _start():
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()

    def _trace(self, dataset_y):
        self._traces.setData(dataset_y)
        self._canvas.setXRange(0, 1000, padding=0)
        self._canvas.setYRange(0, 1024, padding=0)

    def animation(self, running_data):
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: self.update(running_data))
        timer.start()
        self._start()

    def update(self, input_data):
        self._data.append(input_data)
        _new_data = np.array(self._data, dtype='float64')
        self._trace(_new_data)
        self._app.processEvents()

        self._cnt = self._cnt + 1
        if len(self._data) > 1000:
            self._data.clear()


if __name__ == '__main__':
    p = MyPlotWindow()
    p.animation(500)
