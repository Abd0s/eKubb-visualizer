"""Worker thread that handles communication with data sources through the serial interface.

"""
import logging

import serial
from PyQt5 import QtCore

from coms import coms_protocol, messages

logger = logging.getLogger(__name__)


class SerialWorker(QtCore.QObject):
    """The Qt thread for communication over the serial interface

    Attributes:
        port: The serial port to connect to.
    """

    block_fall = QtCore.pyqtSignal(int)

    def __init__(self, port: str) -> None:
        super().__init__()
        self.port = port
        self.setObjectName("SerialWorker")

    def run(self) -> None:
        """Ran when the thread is started"""
        # Open COM port
        try:
            self.serial_connection = serial.Serial(self.port)
        except serial.SerialException:
            logger.error(f"Failed to open COM on port {self.port}")
            return

        logger.info(
            f"Opened COM on port {self.port} with device {self.serial_connection.name}"
        )

        # Establish connection with Handshake
        self.handshake()

        # Handle incoming messages in a loop
        while True:
            try:
                message = self.read_message(acknowledge=True)
            except serial.SerialException:
                logger.error("Error reading from serial, closing port")
                break

            match message:
                case messages.BlockFall():
                    self.block_fall.emit(message.block_index)
                case messages.Log():
                    logger.info(f"Log code from MCU: {message.log_code}")
                case messages.Reset():
                    logger.error("Microcontroller reset, likely semaphore token runout")
                    break

        logger.info("Serial worker thread exiting")

    def handshake(self) -> None:
        """Performs the handshake transaction.

        The following strategy is used:
            1. Spin until Handshake message from microcontroller.
            2. On handshake message recieved, send back HandshakeConfirm message.
        """
        logger.info("Waiting for handshake message")
        # Spin until handshake message is recieved
        while not isinstance(self.read_message(acknowledge=False), messages.Handshake):
            logger.debug("Non handshake message received")

        # Send confirm message for handshake
        self.serial_connection.write(messages.HandshakeConfirm.encode())
        logger.info("Handshake complete")

    def read_message(
        self, acknowledge: bool = True
    ) -> coms_protocol.BaseMessage | None:
        """Tries to read and decode a message from the serial interface.

        The following strategy is used:
            1. Read bytes until startbyte read, read 1 more byte (opcode) and map to message and get size, read size,
               read 1 more byte and check if endbyte.
            2. If no end byte, discard message and log error.
            3. If no opcode mapping discard, log error.

        Args:
            acknowledge: True if an acknowledge message should be sent back after a message has been received. Defaults to True.

        Returns:
            If succesfully received and decoden an message, an corresponding message instance. Else returns `None`.
        """
        logger.debug("Reading message...")

        # Read and throw away bytes until start byte
        self.serial_connection.read_until(expected=coms_protocol.start_byte)
        logger.debug("Read start byte")
        # Read opcode
        opcode = int.from_bytes(
            self.serial_connection.read(1), "little"
        )  # endinness doesn't matter
        # Map opcode to message
        try:
            message_type = messages.opcode_message_mapping[opcode]
        except KeyError:
            logging.error(f"Invalid opcode {opcode}, no message mapped")
            return

        # Read message data
        message_data = self.serial_connection.read(message_type.size())

        # Check endbyte at expected position
        if self.serial_connection.read(1) != coms_protocol.end_byte:
            logging.error(
                f"Error decoding message {message_type.__name__}: no endbyte at expected position. Discarding message"
            )
            return

        # Decode message
        message = message_type(data=message_data)

        # Acknowledge message
        if acknowledge:
            self.serial_connection.write(messages.Acknowledge.encode())

        logger.debug(f"Read message: {message_type.__name__}")

        return message
