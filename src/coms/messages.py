import inspect
import sys

from coms import coms_protocol


class Handshake(coms_protocol.BaseMessage):
    opcode = 1


class HandshakeConfirm(coms_protocol.BaseMessage):
    opcode = 2
    test: coms_protocol.U16
    test1: coms_protocol.U8


# Predicate to make sure the classes only come from the module in question
def pred(c):
    return inspect.isclass(c) and c.__module__ == pred.__module__


# fetch all members of module __name__ matching 'pred'
messages = inspect.getmembers(sys.modules[__name__], pred)

message_opcode_mapping = {
    message[1].opcode: message[1] for message in messages
}
