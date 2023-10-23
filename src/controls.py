import logging
from custom_widgets import logs_widget

from PyQt5 import QtWidgets
from serial.tools import list_ports
import serial

logger = logging.getLogger(__name__)


class ControlWidget(QtWidgets.QWidget):

    def __init__(self, game_visualizer_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Make dynamic basd on screen size
        self.setFixedWidth(400)

        self.game_visualizer_widget = game_visualizer_widget
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(logs_widget.configure_logging())

        self.device_selector = QtWidgets.QComboBox()
        for device in list_ports.comports():
            self.device_selector.addItem(device.device)
        self.layout.addWidget(self.device_selector)
        devices_refresh_button = QtWidgets.QPushButton("Refresh")
        devices_refresh_button.clicked.connect(self.refresh_devices_list)
        self.layout.addWidget(devices_refresh_button)

        device_connect_button = QtWidgets.QPushButton("Connect")
        device_connect_button.clicked.connect(self.connect_device)
        self.layout.addWidget(device_connect_button)

        read_button = QtWidgets.QPushButton("Read")
        read_button.clicked.connect(self.read_device)
        self.layout.addWidget(read_button)

        button = QtWidgets.QPushButton("Press Me!")
        button.clicked.connect(self.game_visualizer_widget.update_function)
        self.layout.addWidget(button)

    def connect_device(self):
        self.serial_connection = serial.Serial(self.device_selector.currentText())
        logging.info(self.serial_connection.name)

    def read_device(self):
        logger.info(self.serial_connection.read())

    def refresh_devices_list(self):
        self.device_selector.clear()
        for i in list_ports.comports():
            self.device_selector.addItem(i.device)
