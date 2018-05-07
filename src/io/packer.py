import struct
import src.io.config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship
import src.config as config

class Packer:

    def pack_relation(relation: Relationship, in_use=True) -> bytes:
        """
        Packs relation to bytes
        :return:
        """
        first_node = relation.first_node.id
        second_node = relation.second_node.id
        type = True
        if relation.first_prev_rel == config.INV_ID:
            first_prev_relation = config.INV_ID
        else:
            first_prev_relation = relation.first_prev_rel.id

        if relation.second_prev_rel == config.INV_ID:
            second_prev_relation = config.INV_ID
        else:
            second_prev_relation = relation.second_prev_rel.id

        if relation.first_next_rel == config.INV_ID:
            first_next_relation = config.INV_ID
        else:
            first_next_relation = relation.first_next_rel.id

        if relation.second_next_rel == config.INV_ID:
            second_next_realtion = config.INV_ID
        else:
            second_next_realtion = relation.second_next_rel.id

        if relation.next_prop == config.INV_ID:
            property = config.INV_ID
        else:
            property = relation.next_prop.id

        label = relation.label.id
        return struct.pack("? ? i i i i i i i i",in_use,type, first_node,second_node, label,property,first_prev_relation,first_next_relation,second_prev_relation,second_next_realtion)

    def pack_label(value_pointer: int, label: Label, in_use=True) -> bytes:
        """
        Packs label to bytes
        :param label:
        :return:
        """
        value = value_pointer
        repr = struct.pack("?i", in_use, value)
        return repr

    def pack_node(node: Node, in_use=True) -> bytes:
        """
        Packs node to bytes
        :return:
        """
        label = node.label.id
        if node.next_prop == config.INV_ID:
            property = config.INV_ID
        else:
            property = node.next_prop.id

        if node.next_rel == config.INV_ID:
            relation = config.INV_ID
        else:
            relation = node.next_rel.id

        return struct.pack("? i i i",in_use,label,property,relation)

    def pack_property_inline(property: Property, in_use=True) -> bytes:
        """
        Packs property with inline store to bytes
        :return:
        """
        key = property.label.id
        if(property.next_prop == config.INV_ID):
            next = property.next_prop
        else:
            next = property.next_prop.id
        if property.type == PropertyType.FLOAT:
            return struct.pack("? i i f i", in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.CHAR:
            return struct.pack("? i i p i", in_use, property.type.value, key, bytes(property.value,encoding="utf8"), next)
        elif property.type == PropertyType.BOOL:
            return struct.pack("? i i ? i",  in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.BYTE:
            return struct.pack("? i i c i",  in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.INT:
            return struct.pack("? i i i i",  in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.SHORT:
            return struct.pack("? i i h i",  in_use, property.type.value, key, property.value, next)


    def pack_property_store(value_pointer: int, property: Property, in_use=True) -> bytes:
        """
        Packs property with dynamic store to bytes
        :param property:
        :return:
        """
        key = property.label.id
        if(property.next_prop == config.INV_ID):
            next = property.next_prop
        else:
            next = property.next_prop.id
        return struct.pack("? i i i i", in_use, property.type.value, key, value_pointer, next)

    def pack_value(next_pointer: int, value: str, in_use=True) -> bytes:
        """
        Packs a string into Dynamic_Store format
        Divides input string into chunks 24 bytes (adds padding if len(value)<24)
        :return: concatenated Dynamic_store formatted bytes
        """
        data = bytes(value, encoding="utf8")
        repr = struct.pack("? i 24p", in_use, next_pointer, data)
        return repr