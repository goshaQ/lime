import struct
import config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship


class Packer:

    def pack_relation(relation: Relationship) -> bytes:
        """
        Packs relation to bytes
        :return:
        """
        in_use = True
        first_node = relation.first_node.id
        second_node = relation.second_node.id
        type = True
        first_prev_relation = relation.first_prev_rel.id
        first_next_relation = relation.first_next_rel.id
        second_prev_relation = relation.second_prev_rel.id
        second_next_realtion = relation.second_next_rel.id
        property = relation.next_prop.id
        label = relation.label
        return struct.pack("? ? i i i i i i i i",in_use,type, first_node,second_node, label,property,first_prev_relation,first_next_relation,second_prev_relation,second_next_realtion)

    def pack_label(value_pointer: int, label: Label) -> bytes:
        """
        Packs label to bytes
        :param label:
        :return:
        """
        in_use = True
        value = value_pointer
        repr = struct.pack("?i", in_use, value)
        return repr

    def pack_node(node: Node) -> bytes:
        """
        Packs node to bytes
        :return:
        """
        in_use = True
        label = node.label
        property = node.next_prop
        relation = node.next_rel
        return struct.pack("? i i i",in_use,label,property,relation)

    def pack_property_inline(property: Property) -> bytes:
        """
        Packs property with inline store to bytes
        :return:
        """
        in_use = True
        key = property.label.id
        next = property.next_prop
        if property.type == PropertyType.FLOAT:
            return struct.pack("? i i f i", in_use, property.type, key, property.value, next)
        elif property.type == PropertyType.CHAR:
            return struct.pack("? i i c i", in_use, property.type, key, property.value, next)
        elif property.type == PropertyType.BOOL:
            return struct.pack("? i i ? i",  in_use, property.type, key, property.value, next)
        elif property.type == PropertyType.BYTE:
            return struct.pack("? i i c i",  in_use, property.type, key, property.value, next)
        elif property.type == PropertyType.INT:
            return struct.pack("? i i i i",  in_use, property.type, key, property.value, next)
        elif property.type == PropertyType.SHORT:
            return struct.pack("? i i h i",  in_use, property.type, key, property.value, next)


    def pack_property_store(value_pointer: int, property: Property) -> bytes:
        """
        Packs property with dynamic store to bytes
        :param property:
        :return:
        """
        in_use = True
        key = property.label.id
        next = property.next_prop
        return struct.pack("? i i i i", in_use, property.type, key, property.value, next)

    def pack_value(pointer: int, value: str) -> bytes:
        """
        Packs a string into Dynamic_Store format
        Divides input string into chunks 24 bytes (adds padding if len(value)<24)
        :return: concatenated Dynamic_store formatted bytes
        """
        blocks = b""
        for i in range(0, len(value), 24):
            pointer = pointer + cfg.STORE_SIZE
            in_use = True
            data = bytes(value[i:i + 24], encoding="utf8")
            blocks = blocks + struct.pack("? i 24p", in_use, pointer, data)
        return blocks