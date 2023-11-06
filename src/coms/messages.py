"""Specificate of messages, only `HandshakeConfirm` and `Acknowledge` should be sent from the hostcomputer

"""
import inspect
import sys

from coms import coms_protocol


class Handshake(coms_protocol.BaseMessage):
    """Initial handshake request message, should be responded to with `HandshakeConfirm`"""

    opcode = 1


class HandshakeConfirm(coms_protocol.BaseMessage):
    """Confirms the handshake, should be sent from the hostcomputer"""

    opcode = 2


class Acknowledge(coms_protocol.BaseMessage):
    """Confirms receival of a message, should be sent from the hostcomputer"""

    opcode = 3


class BlockFall(coms_protocol.BaseMessage):
    """Indicates a block has fallen

    Attributes:
        block_index: The index of the fallen block
    """

    opcode = 4
    block_index: coms_protocol.U8


# Predicate to make sure the classes only come from the module in question
def pred(c):
    return inspect.isclass(c) and c.__module__ == pred.__module__


# fetch all members of module __name__ matching 'pred'
messages: list[tuple[str, type[coms_protocol.BaseMessage]]] = inspect.getmembers(
    sys.modules[__name__], pred
)

opcode_message_mapping: dict[int, type[coms_protocol.BaseMessage]] = {
    message[1].opcode: message[1] for message in messages
}
