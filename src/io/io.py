import os
import _io
import src.config as cfg

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship

from src.io.packer import Packer
from src.io.unpacker import Unpacker


class Io:
    def __init__(self, ):
        if not os.path.exists(cfg.PATH):
            os.makedirs(cfg.PATH)

        self.nodes = open(os.path.join(cfg.PATH, cfg.NODE_FILENAME), "w+b")
        self.labels = open(os.path.join(cfg.PATH, cfg.LABEL_FILENAME), "w+b")
        self.properties = open(os.path.join(cfg.PATH, cfg.PROPERTY_FILENAME), "w+b")
        self.relations = open(os.path.join(cfg.PATH, cfg.RELATIONSHIP_FILENAME), "w+b")
        self.store = open(os.path.join(cfg.PATH, cfg.STORE_FILENAME), "w+b")
        self.last_node_id = int(os.stat(os.path.join(cfg.PATH, cfg.NODE_FILENAME)).st_size / cfg.NODE_SIZE)
        self.last_relation_id = int(
            os.stat(os.path.join(cfg.PATH, cfg.RELATIONSHIP_FILENAME)).st_size / cfg.RELATION_SIZE)
        self.last_property_id = int(os.stat(os.path.join(cfg.PATH, cfg.PROPERTY_FILENAME)).st_size / cfg.PROPERTY_SIZE)
        self.last_label_id = int(os.stat(os.path.join(cfg.PATH, cfg.LABEL_FILENAME)).st_size / cfg.LABEL_SIZE)
        self.last_store_id = int(os.stat(os.path.join(cfg.PATH, cfg.STORE_FILENAME)).st_size / cfg.STORE_SIZE)

    def get_nodes_by_id(self, nodes: set) -> list:
        """
        Gets nodes by specified id. If input set is empty fetches all nodes
        :param nodes: - set of id's to fetch
        :return: list of nodes with matching id
        """
        if len(nodes) == 0:
            nodes = range(0, self.last_node_id)
        result = []
        for id in nodes:
            node = self.read_node(id)
            if node is not None:
                result.append(node)
        return result

    def get_labels_by_id(self, labels: set) -> list:
        """
        Gets labels by specified id. If input set is empty fetches all labels
        :param labels: - set of id's to fetch
        :return: list of labels with matching id
        """
        if len(labels) == 0:
            labels = range(0, self.last_label_id)
        result = []
        for id in labels:
            label = self.read_label(id)
            if label is not None:
                result.append(label)
        return result

    def get_relations_by_id(self, relations: set) -> list:
        """
        Gets relations by specified id. If input set is empty fetches all relations
        :param relations: - set of id's to fetch
        :return: list of relations with matching id
        """
        if len(relations) == 0:
            relations = range(0, self.last_relation_id)
        result = []
        for id in relations:
            relation = self.read_relation(id)
            if relation is not None:
                result.append(relation)
        return result

    def write_node(self, node: Node) -> Node:
        """
        Writes node to file.
        :param node: to pack
        :return: byte representation of string
        """

        if node.id == cfg.INV_ID:
            node.id = self._get_node_id()
        node.label = self.write_label(node.label)
        if (node.next_prop != cfg.INV_ID) and (node.next_prop is not None):
            node.next_prop = self.write_property(node.next_prop)
        value = Packer.pack_node(node)
        self._write_bytes(self.nodes, node.id * cfg.NODE_SIZE, value)

        return node

    def write_label(self, label: Label) -> Label:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param label: - to write
        :return label with generated id
        """
        if label.id == cfg.INV_ID:
            label.id = self._get_label_id()
        store_pointer = self.write_store(label.value)
        value = Packer.pack_label(store_pointer, label)
        self._write_bytes(self.labels, label.id * cfg.LABEL_SIZE, value)
        return label

    def write_property(self, property: Property) -> Property:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param property: - property to write
        """

        if property.id == cfg.INV_ID:
            property.id = self._get_property_id()
        if property.next_prop is not None:
            property.next_prop = self.write_property(property.next_prop)
        if property.label.id == cfg.INV_ID:
            property.label = self.write_label(property.label)
        if property.type.value == PropertyType.STRING.value:
            store_pointer = self.write_store(property.value)
            value = Packer.pack_property_store(store_pointer, property)
        else:
            value = Packer.pack_property_inline(property)

        self._write_bytes(self.properties, property.id * cfg.PROPERTY_SIZE, value)
        return property

    def write_relation(self, relation: Relationship) -> Relationship:
        """
        Writes relation to file.
        :param relation: - relation written
        """
        if relation.next_prop is not None:
            relation.next_prop = self.write_property(relation.next_prop)

        if relation.id == cfg.INV_ID:
            relation.id = self._get_relation_id()
        relation.label = self.write_label(relation.label)

        if relation.first_node is not None:
            first_node = self.read_node(relation.first_node.id)
            if first_node.next_rel is None:
                first_node.next_rel = relation
                self.write_node(first_node)
            else:
                relation = self._update_next_rel(first_node, relation)

        if relation.second_node is not None:
            second_node = self.read_node(relation.second_node.id)
            if second_node.next_rel is None:
                second_node.next_rel = relation

                self.write_node(second_node)
            else:
                relation = self._update_next_rel(second_node, relation)

        value = Packer.pack_relation(relation)
        self._write_bytes(self.relations, relation.id * cfg.RELATION_SIZE, value)
        return relation

    def _update_next_rel(self, node: Node, relation: Relationship):
        next_rel = self.read_relation(node.next_rel)
        node.next_rel = relation.id
        if next_rel.second_node.id == node.id:
            next_rel.second_prev_rel = relation.id
        if next_rel.first_node.id == node.id:
            next_rel.first_prev_rel = relation.id
        self.write_node(node)
        value = Packer.pack_relation(next_rel)
        self._write_bytes(self.relations, next_rel.id * cfg.RELATION_SIZE, value)
        if relation.first_node.id == node.id:
            relation.first_next_rel = next_rel
        if relation.second_node.id == node.id:
            relation.second_next_rel = next_rel
        return relation

    def write_store(self, value: str) -> int:
        """
        Writes values as dynamic store and returns pointer to first chunk of dynamic store
        :param value:  - string to write
        """
        first_pointer = self._get_store_id()
        pointer = first_pointer
        for i in range(0, len(value) - 24, 24):
            next_pointer = self._get_store_id()
            store = Packer.pack_value(next_pointer, value[:24])
            value = value[23:]
            self._write_bytes(self.store, pointer * cfg.STORE_SIZE, store)
            pointer = next_pointer
        next_pointer = cfg.INV_ID
        store = Packer.pack_value(next_pointer, value[:24])
        self._write_bytes(self.store, pointer * cfg.STORE_SIZE, store)
        return first_pointer

    @staticmethod
    def _write_bytes(file, pointer: int, data: bytes):
        """
        Writes data to file with given offset
        :param file: file object to write to
        :param pointer: offset
        :param data: bytes to write
        :return: None
        """
        file.seek(pointer)
        file.write(data)

    def read_node(self, id: int) -> Node or None:
        """
        Reads single node by it's id
        :param id: offset of node to read
        :return: Node unpacked
        """

        if id > self.last_node_id:
            raise Exception('Property ID is out of range')
        node_bytes = self._read_bytes(self.nodes, id, cfg.NODE_SIZE)
        in_use, label_id, property, relation_id = Unpacker.unpack_node(node_bytes)
        if in_use:
            label = self.read_label(label_id)
            if property != cfg.INV_ID:
                property = self.read_property(property)
            else:
                property = None
            if relation_id == cfg.INV_ID:
                relation_id = None
            return Node(id, label, property, relation_id)
        else:
            return None

    def read_label(self, id) -> Label or None:
        """
        Reads single label by it's id
        :param id: offset of label to read
        :return: Label unpacked
        """
        if id > self.last_label_id:
            raise Exception('Label ID is out of range')

        label_bytes = self._read_bytes(self.labels, id, cfg.LABEL_SIZE)

        in_use, store_id = Unpacker.unpack_label(label_bytes)
        if in_use:
            value = self.read_store(store_id)
            return Label(id, value)
        else:
            return None

    def read_property(self, id: int) -> Property or None:
        """
        Reads single property by it's id
        :param id: offset of property to read
        :return: Property unpacked
        """
        if id > self.last_property_id:
            raise Exception('Property ID is out of range')
        property_bytes = self._read_bytes(self.properties, id, cfg.PROPERTY_SIZE)
        in_use, type, label, value, next_property = Unpacker.unpack_property(property_bytes)
        if type == PropertyType.STRING.value:
            value = self.read_store(value)
        if type == PropertyType.FLOAT.value:
            value = float(value)
        if type == PropertyType.CHAR.value:
            value = value.decode("utf8")
        if in_use:
            if label != cfg.INV_ID:
                label = self.read_label(label)
            else:
                label = None
            if next_property != cfg.INV_ID:
                next_property = self.read_property(next_property)
            else:
                next_property = None
            return Property(id, PropertyType(type), label, value, next_property)
        else:
            return None

    def read_relation(self, id) -> Relationship or None:
        """
        Reads single relation by it's id
        :param id: offset of relation to read
        :return: Relation unpacked
        """
        if id > self.last_relation_id:
            raise Exception('Relation ID is out of range')

        relation_bytes = self._read_bytes(self.relations, id, cfg.RELATION_SIZE)
        in_use, type, first_node, second_node, label, property, first_prev_relation, first_next_relation, \
        second_prev_relation, second_next_relation = Unpacker.unpack_relation(relation_bytes)
        if in_use:
            label = self.read_label(label)
            if property != cfg.INV_ID:
                property = self.read_property(property)
            else:
                property = None

            if first_node != cfg.INV_ID:
                first_node = self.read_node(first_node)
            else:
                first_node = None
            if second_node != cfg.INV_ID:
                second_node = self.read_node(second_node)
            else:
                second_node = None
            if first_next_relation == cfg.INV_ID:
                first_next_relation = None
            if second_next_relation == cfg.INV_ID:
                second_next_relation = None
            if first_prev_relation == cfg.INV_ID:
                first_prev_relation = None
            if second_prev_relation == cfg.INV_ID:
                second_prev_relation = None
            return Relationship(id, type, first_node, second_node, label, property,
                                first_prev_relation, first_next_relation, second_prev_relation, second_next_relation)
        else:
            return None

    def read_store(self, id: int) -> str:
        """
        Reads single string from store
        :param id: id of first store block
        :return: string
        """
        value = b""
        if id > self.last_store_id:
            raise Exception('Id is out of range')
        while (id != cfg.INV_ID):
            store_bytes = self._read_bytes(self.store, id, cfg.STORE_SIZE)
            id, chunk = Unpacker.unpack_store(store_bytes)
            value += chunk
        return value.decode("utf8")

    def _read_bytes(self, file: _io.FileIO, offset: int, size: int) -> bytes:
        """
        Read chunks of bytes from filename specified by offset and size
        :param file: to read from
        :param offset: starting location
        :param size: amount of bytes to read
        :return: bytes
        """
        file.seek(offset * size)
        return file.read(size)

    def del_node(self, id: int):
        """
        Delets node and all corresponding properties and relatins
        :param id: id to delete
        :return: None
        """
        node = self.read_node(id)
        new_bytes = Packer.pack_node(node, in_use=False)
        if node.next_prop is not None:
            self.del_property(node.next_prop.id)
        if (node.next_rel is not None):
            self._del_node_relations(node)
        self._write_bytes(self.nodes, id * cfg.NODE_SIZE, new_bytes)

    def _del_node_relations(self, node: Node):
        """
        Recursively deletes all relations of node. Used as helper function of del_node
        :param node: - node to delete relationships from
        :return:
        """
        relations = []
        next_rel = self.read_relation(node.next_rel)
        while(next_rel is not None):
            relations.append(next_rel)
            next_rel = self._find_relations_by_node(node,next_rel)
        for relation in relations:
            new_bytes = Packer.pack_relation(relation, in_use=False)
            self._write_bytes(self.relations,relation.id*cfg.RELATION_SIZE,new_bytes)

    def _find_relations_by_node(self,node: Node,relation:Relationship) -> Relationship:
        """
        Finds correct next relation of node
        :param node:
        :return: next relation
        """
        if relation.first_node.id == node.id:
            if relation.first_next_rel is not None:
                return self.read_relation(relation.first_next_rel)
        if relation.second_node.id == node.id:
            if relation.second_next_rel is not None:
                return self.read_relation(relation.second_next_rel)
        return None

    def del_relation(self, id: int):
        relation = self.read_relation(id)
        new_bytes = Packer.pack_relation(relation, in_use=False)
        self._write_bytes(self.relations, id * cfg.RELATION_SIZE, new_bytes)
        if relation.next_prop is not None:
            self.del_property(relation.next_prop.id)

        if (relation.second_next_rel is not None) and (relation.second_prev_rel is not None):
            second_next_rel = self.read_relation(relation.second_next_rel)
            second_prev_rel = self.read_relation(relation.second_prev_rel)
            self._swap_relation_pointer(second_next_rel, second_prev_rel)

        elif (relation.second_next_rel is not None) and (relation.second_prev_rel is None):
            second_next_rel = self.read_relation(relation.second_next_rel)
            self._fix_next_rel(relation, second_next_rel)

        elif (relation.second_prev_rel is not None) and (relation.second_next_rel is None):
            second_prev_rel = self.read_relation(relation.second_prev_rel)
            self._fix_prev_rel(relation, second_prev_rel)

        if (relation.first_next_rel is not None) and (relation.first_prev_rel is not None):
            first_next_rel = self.read_relation(relation.first_next_rel)
            first_prev_rel = self.read_relation(relation.first_prev_rel)
            self._swap_relation_pointer(first_next_rel, first_prev_rel)

        elif (relation.first_next_rel is not None) and (relation.first_prev_rel is None):
            first_next_rel = self.read_relation(relation.first_next_rel)
            self._fix_next_rel(relation, first_next_rel)

        elif (relation.first_prev_rel is not None) and (relation.first_next_rel is None):
            first_prev_rel = self.read_relation(relation.first_prev_rel)
            self._fix_prev_rel(relation, first_prev_rel)

        node2 = self.read_node(relation.second_node.id)
        node1 = self.read_node(relation.first_node.id)
        self._fix_node_rel(relation, node1)
        self._fix_node_rel(relation, node2)

    def _fix_node_rel(self, current: Relationship, node: Node):
        if node.id == current.first_node.id:
            if node.next_rel == current.id:
                node.next_rel = current.first_next_rel
        if node.id == current.second_node.id:
            if node.next_rel == current.id:
                node.next_rel = current.second_next_rel
        self.write_node(node)

    def _fix_next_rel(self, current: Relationship, next_rel: Relationship):
        """
        Sets next_rel prev pointer to INV_ID
        :param current:
        :param next_rel:
        :return:
        """
        if (current.second_node == next_rel.second_node):
            next_rel.second_prev_id = cfg.INV_ID
        elif (current.second_node == next_rel.first_node):
            next_rel.first_prev_id = cfg.INV_ID
        prev_packed = Packer.pack_relation(next_rel)
        self._write_bytes(self.relations, next_rel.id * cfg.RELATION_SIZE, prev_packed)

    def _fix_prev_rel(self, current: Relationship, prev_rel: Relationship):
        """
        Sets prev_rel next pointer to INV_ID
        :param current:
        :param prev_rel:
        :return:
        """
        if (current.second_node == prev_rel.second_node):
            prev_rel.second_next_id = cfg.INV_ID
        elif (current.second_node == prev_rel.first_node):
            prev_rel.first_next_id = cfg.INV_ID
        prev_packed = Packer.pack_relation(prev_rel)
        self._write_bytes(self.relations, prev_rel.id * cfg.RELATION_SIZE, prev_packed)

    def _swap_relation_pointer(self, next: Relationship, prev: Relationship):
        """
        Swaps pointer of two relations. Helper function for deletion of relation
        :param next:
        :param prev:
        :return:
        """
        if prev.second_node == next.second_node:
            prev.second_next_rel = next.id
            next.second_prev_rel = prev.id
        elif prev.first_node == next.first_node:
            prev.first_next_rel = next.id
            next.first_prev_rel = prev.id
        elif prev.first_node == next.second_node:
            prev.first_next_rel = next.id
            next.second_prev_rel = prev.id
        elif prev.second_node == next.first_node:
            prev.second_next_rel = next.id
            next.first_prev_rel = prev.id
        else:
            raise Exception('No same nodes to swap')

        second_prev_rel_packed = Packer.pack_relation(prev)
        second_next_rel_packed = Packer.pack_relation(next)
        self._write_bytes(self.relations, next.id * cfg.RELATION_SIZE, second_next_rel_packed)
        self._write_bytes(self.relations, prev.id * cfg.RELATION_SIZE, second_prev_rel_packed)

    def del_property(self, id: int):
        """
        Marks signle property as unsued
        :param id:
        :return:
        """
        property = self.read_property(id)
        if property.type == PropertyType.STRING:
            new_bytes = Packer.pack_property_store(cfg.INV_ID, property, in_use=False)
        else:
            new_bytes = Packer.pack_property_inline(property, in_use=False)
        if property.next_prop is not None:
            self.del_property(property.next_prop.id)
        self._write_bytes(self.properties, id * cfg.PROPERTY_SIZE, new_bytes)

    def del_store(self, id: int):
        """
        Marks single string as unused
        :param id:
        :return:
        """
        id, value = Unpacker.unpack_store(self._read_bytes(self.store, id, cfg.STORE_SIZE))
        if id != cfg.INV_ID:
            self.del_store(id)
        new_bytes = Packer.pack_value(id, value, in_use=False)
        self._write_bytes(self.store, id * cfg.STORE_SIZE, new_bytes)

    def _get_label_id(self) -> int:
        """
        Generates new pointer for label
        :return: pointer to label
        """
        pointer = self.last_label_id
        self.last_label_id += 1
        return pointer

    def _get_node_id(self):
        """
        Generates new pointer for node
        :return: pointer to node
        """
        pointer = self.last_node_id
        self.last_node_id += 1
        return pointer

    def _get_store_id(self):
        """
        Generates new pointer for store
        :return: pointer to store
        """
        pointer = self.last_store_id
        self.last_store_id += 1
        return pointer

    def _get_property_id(self):
        """
        Generates new pointer for property
        :return: pointer to property
        """
        pointer = self.last_property_id
        self.last_property_id += 1
        return pointer

    def _get_relation_id(self) -> int:
        pointer = self.last_relation_id
        self.last_relation_id += 1
        return pointer
