"""Microcontroller-hostcomputer communication protocol base implemantation.

"""
import inspect
import typing

start_byte: bytes = b"\x2B"
end_byte: bytes = b"\x2D"


class BaseMessage:
    opcode: int = 0

    def __init__(self, data: bytes, endian: typing.Literal["little", "big"] = "little"):
        """Constructs a message instance from the given bytes sequence.

        The lenght of the byte sequences must match `.size()`. Start and end bytes should not be included.

        Args:
            data: The byte sequence to construct the message from. Must be of length `.size()`
            endian: The endianness of the data. Defaults to "little".

        Raises:
            ValueError: Raised when the length of data does not match `.size()`
        """
        if len(data) != self.size():
            raise ValueError(
                f"The provided data does not match the message size. Expected {self.size}, Received {len(data)}"
            )

        decode_pointer = 0
        for item in inspect.get_annotations(
            type(self)
        ).items():  # Ignores inherited annotations so opcode etc. aren't included
            self.__setattr__(
                item[0],
                item[1].decode(
                    data[decode_pointer : decode_pointer + item[1].size], endian
                ),
            )
            decode_pointer += item[1].size

    @classmethod
    def encode(cls) -> bytes:
        """Encodes the messages as a byte sequences, ignoring any arguments.

        The resulting byte sequences has the `start_byte` - `opcode` - end_byte structure.

        Raises:
            ValueError: Raised when the opcode is not encodeable into 1 byte, in other words bigger than 255.

        Returns:
            The encoded bytes sequence.
        """
        if cls.opcode > 255:
            raise ValueError(
                f"Invalid opcode, should be 1 byte long between 0, 255. Received {cls.opcode}"
            )

        return (
            start_byte + cls.opcode.to_bytes(1, "little") + end_byte
        )  # endian doesn't matter for opcode

    @classmethod
    def size(cls) -> int:
        """Returns the size of the message arguments in bytes.

        Returns:
            The size of the message arguments in bytes.
        """
        size = 0
        for i in inspect.get_annotations(cls).values():
            size += i.size
        return size


class I8:
    size = 1

    @classmethod
    def decode(
        cls, data: bytes, endian: typing.Literal["little", "big"] = "little"
    ) -> int:
        if len(data) != cls.size:
            raise ValueError(
                f"The provided data does not match the type size. Expected {cls.size}, Received {len(data)}"
            )
        return int.from_bytes(data, endian, signed=True)


class I16:
    size = 2

    @classmethod
    def decode(
        cls, data: bytes, endian: typing.Literal["little", "big"] = "little"
    ) -> int:
        if len(data) != cls.size:
            raise ValueError(
                f"The provided data does not match the type size. Expected {cls.size}, Received {len(data)}"
            )
        return int.from_bytes(data, endian, signed=True)


class U8:
    size = 1

    @classmethod
    def decode(
        cls, data: bytes, endian: typing.Literal["little", "big"] = "little"
    ) -> int:
        if len(data) != cls.size:
            raise ValueError(
                f"The provided data does not match the type size. Expected {cls.size}, Received {len(data)}"
            )
        return int.from_bytes(data, endian, signed=False)


class U16:
    size = 2

    @classmethod
    def decode(
        cls, data: bytes, endian: typing.Literal["little", "big"] = "little"
    ) -> int:
        if len(data) != cls.size:
            raise ValueError(
                f"The provided data does not match the type size. Expected {cls.size}, Received {len(data)}"
            )
        return int.from_bytes(data, endian, signed=False)


class CHAR:
    size = 1

    @classmethod
    def decode(
        cls, data: bytes, endian: typing.Literal["little", "big"] = "little"
    ) -> str:
        if len(data) != cls.size:
            raise ValueError(
                f"The provided data does not match the type size. Expected {cls.size}, Received {len(data)}"
            )
        return data.decode()