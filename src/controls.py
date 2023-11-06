import logging

from PyQt5 import QtWidgets, QtCore
from serial.tools import list_ports
from coms import serial_worker

from custom_widgets import logs_widget, game_visualizer

logger = logging.getLogger(__name__)


class ControlWidget(QtWidgets.QWidget):
    def __init__(
        self,
        game_visualizer_widget: game_visualizer.GameVisualizerWidget,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # TODO: Make dynamic basd on screen size
        self.setFixedWidth(600)

        self.game_visualizer_widget = game_visualizer_widget
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(logs_widget.configure_logging())

        # Device selector
        self.device_selector = QtWidgets.QComboBox()
        for device in list_ports.comports():
            self.device_selector.addItem(device.device)
        self.layout.addWidget(self.device_selector)
        # Device refresh button
        devices_refresh_button = QtWidgets.QPushButton("Refresh")
        devices_refresh_button.clicked.connect(self.refresh_devices_list)
        self.layout.addWidget(devices_refresh_button)
        # Device connect button
        self.device_connect_button = QtWidgets.QPushButton("Connect")
        self.device_connect_button.clicked.connect(self.connect_device)
        self.layout.addWidget(self.device_connect_button)
        # Device disconnect button
        self.device_disconnect_button = QtWidgets.QPushButton("Disconnect")
        self.device_disconnect_button.setEnabled(False)
        self.device_disconnect_button.clicked.connect(self.disconnect_device)
        self.layout.addWidget(self.device_disconnect_button)

        # button = QtWidgets.QPushButton("Press Me!")
        # button.clicked.connect(self.game_visualizer_widget.update_function)
        # self.layout.addWidget(button)

    def connect_device(self):
        # Start background thread to hanlde coms with microcontroller over serial
        self.device_disconnect_button.setEnabled(True)

        self.thread = QtCore.QThread()
        self.worker = serial_worker.SerialWorker(self.device_selector.currentText())
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        self.device_connect_button.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.device_connect_button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.device_disconnect_button.setEnabled(False)
        )

        # Custom signals and slots
        self.worker.block_fall.connect(self.handle_block_fall)

        self.thread.start()

    def handle_block_fall(self, index: int):
        self.game_visualizer_widget.fall_block(index)

    def disconnect_device(self):
        self.thread.exit()
        logger.info("Killed serial thread")

    def refresh_devices_list(self):
        self.device_selector.clear()
        for i in list_ports.comports():
            self.device_selector.addItem(i.device)
