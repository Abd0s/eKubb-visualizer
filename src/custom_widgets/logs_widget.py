import logging
from PyQt5 import QtCore, QtWidgets


class QTextEditLogger(logging.Handler, QtCore.QObject):
    append_plain_text = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit()
        self.widget.setReadOnly(True)
        self.append_plain_text.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.append_plain_text.emit(msg)


def configure_logging() -> QtWidgets.QPlainTextEdit:
    log_text_box = QTextEditLogger()

    # log to text box
    log_text_box.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(message)s")
    )
    logging.getLogger().addHandler(log_text_box)
    logging.getLogger().setLevel(logging.DEBUG)

    # log to file
    file_handler = logging.FileHandler("ekubb.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(threadName)s %(module)s %(funcName)s %(message)s"
        )
    )
    logging.getLogger().addHandler(file_handler)

    return log_text_box.widget
