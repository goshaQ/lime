import struct
import src.io.config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship


class Unpacker:
    def unpack_store(store: bytes) -> (int,str):
        """
        Gets value from single Dynamic_Store byte
        :return:
        """
        unpacked = struct.unpack("?i24p", store)
        return unpacked[1],unpacked[2]

    def unpack_label(label: bytes) -> int:
        """
        Gets label from single Label bytes
        :param label:
        :return:
        """
        unpacked = struct.unpack("? i",label)
        return unpacked[1]

    def unpack_property(property: bytes) -> (int,int,int):
        """
        Gets property from single Property bytes
        :param property:
        :return:
        """
        unpacked = struct.unpack("? i i i i",property)
        if unpacked[1] == PropertyType.FLOAT.value:
            return struct.unpack("? i i f i", property)[1:]
        elif unpacked[1] == PropertyType.CHAR.value:
            return struct.unpack("? i i p i", property)[1:]
        elif unpacked[1] == PropertyType.BOOL.value:
            return struct.unpack("? i i ? i",  property)[1:]
        elif unpacked[1] == PropertyType.BYTE.value:
            return struct.unpack("? i i c i", property)[1:]
        elif unpacked[1] == PropertyType.INT.value:
            return struct.unpack("? i i i i",  property)[1:]
        elif unpacked[1] == PropertyType.SHORT.value:
            return struct.unpack("? i i h i", property)[1:]
        else:
            return unpacked[1:]

    def unpack_node(id: int,node: bytes) -> (int,int,int):
        """
        Gets node from single Node bytes
        :param node:
        :return:
        """
        unpacked = struct.unpack("? i i i",node)
        return (unpacked[1],unpacked[2],unpacked[3])

    def unpack_relation(id: int,relation: bytes) -> ():
        """
        Gets relation from single Relation bytes
        :param node:
        :return:
        """
        unpacked = struct.unpack("? ? i i i i i i i i", relation)
        return (unpacked[1],unpacked[2],unpacked[3],unpacked[4],unpacked[5],unpacked[6],unpacked[7],unpacked[8],unpacked[9])