import struct
import src.config as cfg

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

    def unpack_label(label: bytes) -> (bool,int):
        """
        Gets label from single Label bytes
        :param label:
        :return:
        """
        unpacked = struct.unpack("? i",label)
        return unpacked

    def unpack_property(property: bytes) -> (bool,int,int,int):
        """
        Gets property from single Property bytes
        :param property:
        :return:
        """
        unpacked = struct.unpack("? i i i i",property)
        if unpacked[1] == PropertyType.FLOAT.value:
            return struct.unpack("? i i f i", property)
        elif unpacked[1] == PropertyType.CHAR.value:
            return struct.unpack("? i i p i", property)
        elif unpacked[1] == PropertyType.BOOL.value:
            return struct.unpack("? i i ? i",  property)
        elif unpacked[1] == PropertyType.BYTE.value:
            return struct.unpack("? i i c i", property)
        elif unpacked[1] == PropertyType.INT.value:
            return struct.unpack("? i i i i",  property)
        elif unpacked[1] == PropertyType.SHORT.value:
            return struct.unpack("? i i h i", property)
        else:
            return unpacked

    def unpack_node(id: int,node: bytes) -> (bool,int,int,int):
        """
        Gets node from single Node bytes
        :param node:
        :return:
        """
        unpacked = struct.unpack("? i i i",node)
        return unpacked

    def unpack_relation(id: int,relation: bytes) -> ():
        """
        Gets relation from single Relation bytes
        :param node:
        :return:
        """
        unpacked = struct.unpack("? ? i i i i i i i i", relation)
        return unpacked