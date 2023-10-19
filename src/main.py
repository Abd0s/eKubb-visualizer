import sys
import logging

from PyQt5 import QtCore, QtWidgets

import controls
import game_visualizer

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.vl = QtWidgets.QVBoxLayout()
        self.frame = QtWidgets.QFrame()
        self.game_visualizer_widget = game_visualizer.GameVisualizerWidget(self.frame)
        self.controls_widget = controls.ControlWidget(self.game_visualizer_widget)
        self.vl.addWidget(self.game_visualizer_widget)

        self.controls_widget_dock = QtWidgets.QDockWidget("Controls", self)
        self.controls_widget_dock.setWidget(self.controls_widget)
        self.controls_widget_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable |
                                              QtWidgets.QDockWidget.DockWidgetFloatable)
        self.controls_widget_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.controls_widget_dock)

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
