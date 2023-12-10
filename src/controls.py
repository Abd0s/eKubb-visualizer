import logging

from PyQt5 import QtWidgets, QtCore
from serial.tools import list_ports
from coms import serial_worker, tcp_receiver_worker

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
        # TCP connect button
        self.tcp_connect_button = QtWidgets.QPushButton("Connect TCP")
        self.tcp_connect_button.clicked.connect(self.connect_tcp)
        self.layout.addWidget(self.tcp_connect_button)
        # TCP disconnect button
        self.tcp_disconnect_button = QtWidgets.QPushButton("Disconnect TCP")
        self.tcp_disconnect_button.setEnabled(False)
        self.tcp_disconnect_button.clicked.connect(self.disconnect_tcp)
        self.layout.addWidget(self.tcp_disconnect_button)
        # Restart game
        self.restart_game_button = QtWidgets.QPushButton("Restart Game")
        self.restart_game_button.clicked.connect(self.restart_game)
        self.layout.addWidget(self.restart_game_button)
        # Reset stick
        self.reset_stick_button = QtWidgets.QPushButton("Reset Stick")
        self.reset_stick_button.clicked.connect(self.reset_stick)
        self.layout.addWidget(self.reset_stick_button)
        # Demo game
        self.demo_game_button = QtWidgets.QPushButton("Demo")
        self.demo_game_button.clicked.connect(self.demo_game)
        self.layout.addWidget(self.demo_game_button)

    def demo_game(self) -> None:
        self.game_visualizer_widget.update_function()

    def reset_stick(self) -> None:
        self.game_visualizer_widget.reset_stick()

    def restart_game(self) -> None:
        self.game_visualizer_widget.reset_scene()
        self.game_visualizer_widget.init_scene()
        self.game_visualizer_widget.renderer.GetRenderWindow().Render()

    def connect_device(self):
        # Start background thread to hanlde coms with microcontroller over serial
        self.device_disconnect_button.setEnabled(True)

        self.serial_thread = QtCore.QThread()
        self.serial_worker = serial_worker.SerialWorker(self.device_selector.currentText())
        self.serial_worker.moveToThread(self.serial_thread)
        # Connect signals and slots
        self.serial_thread.started.connect(self.serial_worker.run)
        self.serial_thread.finished.connect(self.serial_thread.deleteLater)
        self.serial_thread.finished.connect(self.serial_worker.deleteLater)

        self.device_connect_button.setEnabled(False)
        self.serial_thread.finished.connect(
            lambda: self.device_connect_button.setEnabled(True)
        )
        self.serial_thread.finished.connect(
            lambda: self.device_disconnect_button.setEnabled(False)
        )

        # Custom signals and slots
        self.serial_worker.block_fall.connect(self.handle_block_fall)

        self.serial_thread.start()

    def disconnect_device(self):
        self.serial_thread.exit()
        logger.info("Serial thread exit signalled")

    def connect_tcp(self):
        # Start background thread to hanlde coms with microcontroller over serial
        self.tcp_disconnect_button.setEnabled(True)

        self.tcp_thread = QtCore.QThread()
        self.tcp_worker = tcp_receiver_worker.TCPReceiverWorker()
        self.tcp_worker.moveToThread(self.tcp_thread)
        # Connect signals and slots
        self.tcp_thread.started.connect(self.tcp_worker.run)
        self.tcp_thread.finished.connect(self.tcp_thread.deleteLater)
        self.tcp_thread.finished.connect(self.tcp_worker.deleteLater)

        self.tcp_connect_button.setEnabled(False)
        self.tcp_thread.finished.connect(
            lambda: self.tcp_connect_button.setEnabled(True)
        )
        self.tcp_thread.finished.connect(
            lambda: self.tcp_disconnect_button.setEnabled(False)
        )

        # Custom signals and slots
        self.tcp_worker.block_fall.connect(self.handle_block_fall)

        self.tcp_thread.start()

    def disconnect_tcp(self):
        #self.tcp_worker.stop()
        self.tcp_thread.quit()
        #self.tcp_thread.wait()
        logger.info("TCP receiver thread exit signalled")

    def handle_block_fall(self, index: int):
        self.game_visualizer_widget.fall_block(False, index)

    def refresh_devices_list(self):
        self.device_selector.clear()
        for i in list_ports.comports():
            self.device_selector.addItem(i.device)
