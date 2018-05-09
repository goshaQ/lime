import struct
import src.config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship


class Packer:
    @staticmethod
    def pack_relation(relation: Relationship, in_use=True) -> bytes:
        """
        Packs relation to bytes
        :return:
        """
        first_node = relation.first_node.id
        second_node = relation.second_node.id
        direction = relation.is_directed

        if (relation.first_prev_rel == cfg.INV_ID) or (relation.first_prev_rel is None):
            first_prev_relation = cfg.INV_ID
        elif type(relation.first_prev_rel) is Relationship:
            first_prev_relation = relation.first_prev_rel.id
        else:
            first_prev_relation = relation.first_prev_rel

        if (relation.second_prev_rel == cfg.INV_ID) or (relation.second_prev_rel is None):
            second_prev_relation = cfg.INV_ID
        elif type(relation.second_prev_rel) is Relationship:
            second_prev_relation = relation.second_prev_rel.id
        else:
            second_prev_relation = relation.second_prev_rel

        if (relation.first_next_rel == cfg.INV_ID) or (relation.first_next_rel is None):
            first_next_relation = cfg.INV_ID
        elif type(relation.first_next_rel) is Relationship:
            first_next_relation = relation.first_next_rel.id
        else:
            first_next_relation = relation.first_next_rel

        if (relation.second_next_rel == cfg.INV_ID) or (relation.second_next_rel is None):
            second_next_realtion = cfg.INV_ID
        elif type(relation.second_next_rel) is Relationship:
            second_next_realtion = relation.second_next_rel.id
        else:
            second_next_realtion = relation.second_next_rel

        if (relation.next_prop == cfg.INV_ID) or (relation.next_prop is None):
            property = cfg.INV_ID
        else:
            property = relation.next_prop.id

        label = relation.label.id
        return struct.pack("? ? i i i i i i i i", in_use, direction, first_node, second_node, label, property,
                           first_prev_relation, first_next_relation, second_prev_relation, second_next_realtion)

    @staticmethod
    def pack_label(value_pointer: int, label: Label, in_use=True) -> bytes:
        """
        Packs label to bytes
        :param value_pointer:
        :param in_use:
        :param label:
        :return:
        """
        value = value_pointer
        repr = struct.pack("?i", in_use, value)
        return repr

    @staticmethod
    def pack_node(node: Node, in_use=True) -> bytes:
        """
        Packs node to bytes
        :return:
        """
        label = node.label.id
        if node.next_prop is None:
            property = cfg.INV_ID
        else:
            property = node.next_prop.id

        if node.next_rel is None:
            relation = cfg.INV_ID
        elif type(node.next_rel) is Relationship:
            relation = node.next_rel.id
        else:
            relation = node.next_rel
        return struct.pack("? i i i", in_use, label, property, relation)

    @staticmethod
    def pack_property_inline(property: Property, in_use=True) -> bytes:
        """
        Packs property with inline store to bytes
        :return:
        """
        key = property.label.id
        if property.next_prop is None:
            next = cfg.INV_ID
        else:
            next = property.next_prop.id
        if property.type == PropertyType.FLOAT:
            return struct.pack("? i i f i", in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.CHAR:
            return struct.pack("? i i p i", in_use, property.type.value, key, bytes(property.value, encoding="utf8"),
                               next)
        elif property.type == PropertyType.BOOL:
            return struct.pack("? i i ? i", in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.BYTE:
            return struct.pack("? i i c i", in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.INT:
            return struct.pack("? i i i i", in_use, property.type.value, key, property.value, next)
        elif property.type == PropertyType.SHORT:
            return struct.pack("? i i h i", in_use, property.type.value, key, property.value, next)

    @staticmethod
    def pack_property_store(value_pointer: int, property: Property, in_use=True) -> bytes:
        """
        Packs property with dynamic store to bytes
        :param property:
        :return:
        """
        key = property.label.id
        if (property.next_prop == cfg.INV_ID) or (property.next_prop is None):
            next = cfg.INV_ID
        else:
            next = property.next_prop.id
        return struct.pack("? i i i i", in_use, property.type.value, key, value_pointer, next)

    @staticmethod
    def pack_value(next_pointer: int, value: str, in_use=True) -> bytes:
        """
        Packs a string into Dynamic_Store format
        Divides input string into chunks 24 bytes (adds padding if len(value)<24)
        :return: concatenated Dynamic_store formatted bytes
        """
        data = bytes(value, encoding="utf8")
        repr = struct.pack("? i 24p", in_use, next_pointer, data)
        return repr
