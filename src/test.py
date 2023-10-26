from coms import coms_protocol
from coms import messages


testbytes = bytes([0, 5, 0])


test = messages.HandshakeConfirm(testbytes, endian="big")
print(test.test)
print(test.test1)