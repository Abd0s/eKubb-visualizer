from PyQt5 import QtWidgets


class ControlWidget(QtWidgets.QWidget):

    def __init__(self, game_visualizer_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game_visualizer_widget = game_visualizer_widget
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel("Controls"))
        button = QtWidgets.QPushButton("Press Me!")
        button.clicked.connect(self.game_visualizer_widget.update_function)
        layout.addWidget(button)
