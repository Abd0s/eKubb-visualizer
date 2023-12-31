"""PyQt widget that creates all the GUI elements and is used to orchastrite the program state.

This widget is responsible for creating all the GUI elements, creating and communicating with 
the datasource workers such as the serial worker and and updating the game visualisation. 
"""
import logging

from PyQt5 import QtWidgets, QtCore
from serial.tools import list_ports
from coms import serial_worker, tcp_receiver_worker

from custom_widgets import logs_widget, game_visualizer

logger = logging.getLogger(__name__)


class EkkubControlWidget(QtWidgets.QWidget):
    def __init__(
            self,
            game_visualizer_widget: game_visualizer.GameVisualizerWidget,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(600)

        # Main layout
        self.game_visualizer_widget = game_visualizer_widget
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Logs widget
        logs_groupbox = QtWidgets.QGroupBox("Logs")
        self.layout.addWidget(logs_groupbox)
        logs_layout = QtWidgets.QVBoxLayout()
        logs_groupbox.setLayout(logs_layout)
        logs_layout.addWidget(logs_widget.configure_logging())

        # Serial connection group
        serial_connection_groupbox = QtWidgets.QGroupBox("Serial Connection")
        self.layout.addWidget(serial_connection_groupbox)
        serial_connection_layout = QtWidgets.QVBoxLayout()
        serial_connection_groupbox.setLayout(serial_connection_layout)
        # Device selector
        device_selector_layout = QtWidgets.QHBoxLayout()
        self.device_selector = QtWidgets.QComboBox()
        for device in list_ports.comports():
            self.device_selector.addItem(device.device)
        device_selector_layout.addWidget(QtWidgets.QLabel("Select COM device:"))
        device_selector_layout.addWidget(self.device_selector)
        serial_connection_layout.addLayout(device_selector_layout)
        # Device refresh button
        devices_refresh_button = QtWidgets.QPushButton("Refresh")
        devices_refresh_button.clicked.connect(self.refresh_devices_list)
        serial_connection_layout.addWidget(devices_refresh_button)
        # Device connect button
        self.device_connect_button = QtWidgets.QPushButton("Connect Serial")
        self.device_connect_button.clicked.connect(self.connect_device)
        serial_connection_layout.addWidget(self.device_connect_button)
        # Device disconnect button
        self.device_disconnect_button = QtWidgets.QPushButton("Disconnect Serial")
        self.device_disconnect_button.setEnabled(False)
        self.device_disconnect_button.clicked.connect(self.disconnect_device)
        serial_connection_layout.addWidget(self.device_disconnect_button)

        # TCP connection group
        tcp_connection_groupbox = QtWidgets.QGroupBox("TCP Connection")
        self.layout.addWidget(tcp_connection_groupbox)
        tcp_connection_layout = QtWidgets.QVBoxLayout()
        tcp_connection_groupbox.setLayout(tcp_connection_layout)
        # TCP connect button
        self.tcp_connect_button = QtWidgets.QPushButton("Connect TCP")
        self.tcp_connect_button.clicked.connect(self.connect_tcp)
        tcp_connection_layout.addWidget(self.tcp_connect_button)
        # TCP disconnect button
        self.tcp_disconnect_button = QtWidgets.QPushButton("Disconnect TCP")
        self.tcp_disconnect_button.setEnabled(False)
        self.tcp_disconnect_button.clicked.connect(self.disconnect_tcp)
        tcp_connection_layout.addWidget(self.tcp_disconnect_button)

        # Game controls group
        game_controls_groupbox = QtWidgets.QGroupBox("Game controls")
        self.layout.addWidget(game_controls_groupbox)
        game_control_layout = QtWidgets.QVBoxLayout()
        game_controls_groupbox.setLayout(game_control_layout)
        # Team toggle
        toggle_button_layout = QtWidgets.QHBoxLayout()
        self.toggle_playing_team_a_button = QtWidgets.QPushButton("Team A")
        self.toggle_playing_team_b_button = QtWidgets.QPushButton("Team B")
        self.toggle_playing_team_a_button.setDisabled(True)
        self.toggle_playing_team_b_button.clicked.connect(self.toggle_playing_team)
        self.toggle_playing_team_a_button.clicked.connect(self.toggle_playing_team)
        toggle_button_layout.addWidget(QtWidgets.QLabel("Toggle playing team:"))
        toggle_button_layout.addWidget(self.toggle_playing_team_a_button)
        toggle_button_layout.addWidget(self.toggle_playing_team_b_button)
        game_control_layout.addLayout(toggle_button_layout)
        # Restart game
        self.restart_game_button = QtWidgets.QPushButton("Restart Game")
        self.restart_game_button.clicked.connect(self.restart_game)
        game_control_layout.addWidget(self.restart_game_button)
        # Reset stick
        self.reset_stick_button = QtWidgets.QPushButton("Reset Stick")
        self.reset_stick_button.clicked.connect(self.reset_stick)
        game_control_layout.addWidget(self.reset_stick_button)
        # Demo game
        self.demo_game_button = QtWidgets.QPushButton("Demo")
        self.demo_game_button.clicked.connect(self.demo_game)
        game_control_layout.addWidget(self.demo_game_button)

        logger.info("Ready to go...")

    def demo_game(self) -> None:
        """Demo button slot, shows a demo."""
        self.game_visualizer_widget.update_function()

    def reset_stick(self) -> None:
        """Reset stick button slot, resets the stick."""
        self.game_visualizer_widget.reset_stick()

    def restart_game(self) -> None:
        """Restart game button slot, restarts the game."""
        self.game_visualizer_widget.reset_scene()
        self.game_visualizer_widget.init_scene()
        self.game_visualizer_widget.renderer.GetRenderWindow().Render()

    def connect_device(self) -> None:
        """Connect serial button slot, starts the serial worker to the selected COM device."""
        # Start background thread to hanlde coms with microcontroller over serial
        self.device_disconnect_button.setEnabled(True)

        self.serial_thread = QtCore.QThread()
        self.serial_worker = serial_worker.SerialWorker(
            self.device_selector.currentText()
        )
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

    def disconnect_device(self) -> None:
        """Disconnect serial button slot, sends the exit signal to the serial worker thread."""
        self.serial_thread.exit()
        logger.info("Serial thread exit signalled")

    def connect_tcp(self) -> None:
        """Connect TCP button slot, starts the TCP receiver worker."""
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

    def disconnect_tcp(self) -> None:
        """Disconnect TCP button slot, sends the exit signal to the TCP receiver thread."""
        self.tcp_thread.quit()
        logger.info("TCP receiver thread exit signalled")

    def handle_block_fall(self, index: int) -> None:
        """Fall block slot, used from datasource worker threads.

        Args:
            index: The index of the block to fall over.
        """
        self.game_visualizer_widget.fall_block(not self.game_visualizer_widget.playing_team, index)

    def refresh_devices_list(self) -> None:
        """Refresh button slot, refreshes the COM devices list."""
        self.device_selector.clear()
        for i in list_ports.comports():
            self.device_selector.addItem(i.device)

    def toggle_playing_team(self) -> None:
        """Team toggle button slot, Toggle the playing team"""
        if self.toggle_playing_team_b_button.isEnabled():
            # Means team B button is pressed
            self.toggle_playing_team_b_button.setDisabled(True)
            self.toggle_playing_team_a_button.setDisabled(False)

        elif self.toggle_playing_team_a_button.isEnabled():
            # Means team A button is pressed
            self.toggle_playing_team_b_button.setDisabled(False)
            self.toggle_playing_team_a_button.setDisabled(True)

        self.game_visualizer_widget.playing_team = not self.game_visualizer_widget.playing_team
        logger.info(f"Toggled playing team from {not self.game_visualizer_widget.playing_team} to "
                    f"{self.game_visualizer_widget.playing_team}")
