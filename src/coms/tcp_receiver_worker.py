import logging
import socket

from PyQt5 import QtCore

from coms import coms_protocol, messages
import config

logger = logging.getLogger(__name__)


class TCPReceiverWorker(QtCore.QObject):
    block_fall = QtCore.pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("TCPReceiverWorker")
        self.tcp_socket = None
        self.connection = None

    def run(self) -> None:
        # Connect TCP
        logger.info(f"Trying to establish TCP connection: {config.TCP_IP, config.TCP_PORT}")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((config.TCP_IP, config.TCP_PORT))
        self.tcp_socket.listen(1)
        self.tcp_socket.settimeout(20.0)
        try:
            self.connection, addr = self.tcp_socket.accept()
        except TimeoutError:
            logger.error("TCP Connection timed out")
            return

        self.connection.settimeout(2.0)
        logger.info(f"TCP Connected: {self.connection, addr}")

        # Establish connection with Handshake
        while True:
            try:
                self.handshake()
                break
            except TimeoutError:
                logger.debug("Timeout handshake")
                pass

        # Handle incoming messages in a loop
        while True:
            try:
                message = self.read_message(acknowledge=True)
            except TimeoutError:
                logger.debug("Read message time out")
                continue
            except IOError as e:
                logger.error("Error reading from TCP, closing connection.")
                logger.error(e)
                break

            match message:
                case messages.BlockFall():
                    self.block_fall.emit(message.block_index)
                case messages.Log():
                    logger.info(f"Log code from TCP: {message.log_code}")
                case messages.Reset():
                    logger.error("TCP reset")
                    break

        self.connection.close()
        self.tcp_socket.close()

        logger.info("TCP Receiver thread exiting")

    def handshake(self) -> None:
        # Handshake protocol:
        # Spin until Handshake message from microcontroller
        # On handshake message recieved, send back HandshakeConfirm message
        # If any other message received, discard.
        # Tolerate 10 other messages before disconnecting, or 60 seconds.

        logger.info("Waiting for handshake message")
        # Spin until handshake message is received
        while not isinstance(self.read_message(acknowledge=False), messages.Handshake):
            logger.debug("Non handshake message received")

        # Send confirm message for handshake
        self.connection.sendall(messages.HandshakeConfirm.encode())
        logger.info("Handshake complete")

    def read_message(self, acknowledge: bool = True) -> coms_protocol.BaseMessage | None:
        # Message reading strategy:
        # Read bytes until startbyte read, read 1 more byte (opcode) and map to message and get size, read size, read 1 more byte and check if endbyte
        # If no end byte, discard message and log error
        # If no opcode mapping discard, log error
        # If valid read, send ACK message

        logger.debug("Reading message...")

        # Read and throw away bytes until start byte
        while True:
            read_byte = self.connection.recv(1)
            if read_byte == coms_protocol.start_byte:
                break

        logger.debug("Read start byte")
        # Read opcode
        opcode = int.from_bytes(self.connection.recv(1), "little")  # sandiness doesn't matter
        # Map opcode to message
        try:
            message_type = messages.opcode_message_mapping[opcode]
        except KeyError:
            logging.error(f"Invalid opcode {opcode}, no message mapped")
            return

        # Read message data
        message_data = self.connection.recv(message_type.size())

        # Check endbyte at expected position
        if self.connection.recv(1) != coms_protocol.end_byte:
            logging.error(
                f"Error decoding message {message_type.__name__}: no endbyte at expected position. Discarding message"
            )
            return

        # Decode message
        message = message_type(data=message_data)

        # Acknowledge message
        if acknowledge:
            self.connection.sendall(messages.Acknowledge.encode())

        logger.debug(f"Read message: {message_type.__name__}")

        return message
