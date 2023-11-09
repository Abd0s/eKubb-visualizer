import logging

import serial
from PyQt5 import QtCore

from coms import coms_protocol, messages

logger = logging.getLogger(__name__)


class SerialWorker(QtCore.QObject):
    block_fall = QtCore.pyqtSignal(int)

    def __init__(self, port: str) -> None:
        super().__init__()
        self.port = port
        self.setObjectName("SerialWorker")

    def run(self) -> None:
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
                message = self.read_message(acknowledge=False)
            except serial.SerialException:
                logger.error("Error reading from serial, closing port")
                return

            match message:
                case messages.BlockFall():
                    self.block_fall.emit(message.block_index)
                case messages.Log():
                    logger.info(f"Log code from MCU: {message.log_code}")
                case messages.Reset():
                    logger.error("Microcontroller reset, likely semaphore token runout")
                    return

    def handshake(self) -> None:
        # Handshake protocol:
        # Spin until Handshake message from microcontroller
        # On handshake message recieved, send back HandshakeConfirm message
        # If any other message received, discard.
        # Tolerate 10 other messages before disconnecting, or 60 seconds.

        logger.info("Waiting for handshake message")
        # Spin until handshake message is recieved
        while not isinstance(self.read_message(acknowledge=False), messages.Handshake):
            logger.debug("Non handshake message received")

        # Send confirm message for handshake
        self.serial_connection.write(messages.HandshakeConfirm.encode())
        logger.info("Handshake complete")

    def read_message(self, acknowledge: bool = True) -> coms_protocol.BaseMessage | None:
        # Message reading strategy:
        # Read bytes until startbyte read, read 1 more byte (opcode) and map to message and get size, read size, read 1 more byte and check if endbyte
        # If no end byte, discard message and log error
        # If no opcode mapping discard, log error
        # If valid read, send ACK message

        logger.debug("Reading message...")

        # Read and throw away bytes until start byte
        self.serial_connection.read_until(expected=coms_protocol.start_byte)
        logger.debug("Read start byte")
        # Read opcode
        opcode = int.from_bytes(self.serial_connection.read(1), "little")  # sandiness doesn't matter
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
