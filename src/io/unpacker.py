import struct
import src.io.config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
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
        return (unpacked[1],unpacked[2],unpacked[3],unpacked[4])

    def unpack_node(id: int,node: bytes) -> Node:
        """
        Gets node from single Node bytes
        :param node:
        :return:
        """
        unpacked = struct.unpack("? i i i",node)
        return Node(id,unpacked[1],unpacked[2],unpacked[3])

    def unpack_relation(id: int,relation: bytes) -> Relationship:
        """
        Gets relation from single Relation bytes
        :param node:
        :return:
        """
        unpacked = struct.pack("? ? i i i i i i i", relation)
        return Relationship(id,unpacked[1],unpacked[2],unpacked[3],unpacked[4],unpacked[5],unpacked[6],unpacked[7],unpacked[8],unpacked[9])