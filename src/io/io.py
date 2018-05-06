import struct

import _io
import src.io.config as cfg
from src.engine.label import Label

from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship

from src.io.packer import Packer
from src.io.unpacker import Unpacker



class Io:

    def __init__(self,):
        self.nodes = cfg.NODE_FILENAME
        self.labels = cfg.LABEL_FILENAME
        self.properties = cfg.PROPERTY_FILENAME
        self.relations = cfg.RELATION_FILENAME
        self.store = cfg.STORE_FILANAME
        self.last_node_id = self.labels / cfg.LABEL_SIZE
        self.last_relation_id = self.relations / cfg.RELATION_SIZE
        self.last_property_id = self.properties / cfg.PROPERTY_SIZE
        self.last_label_id = self.labels / cfg.LABEL_SIZE
        self.last_store_id = self.store / cfg.STORE_SIZE

    def get_nodes_by_id(self, nodes: set) -> list:
        """
        Gets nodes by specified id. If input set is empty fetches all nodes
        :param nodes: - set of id's to fetch
        :return: list of nodes with matching id
        """
        if len(nodes) == 0:
            nodes = range(0,self.last_node_id,cfg.NODE_SIZE)
        result = []
        for id in nodes:
            result.append(self.read_node(id))
        return result

    def write_node(self, node: Node) -> Node:
        """
        Writes node to file.
        :param node to pack:
        :return: byte represenation of string
        """
        if node.id == INVALID_ID:
            node.id = self._get_node_id()
        value = Packer.pack_node(node)
        self._write_bytes(self.nodes,node.id,value)
        return node

    def write_label(self,label: Label) -> Label:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param property - property to write:
        """
        if label.id == INVALID_ID:
            label.id = self._get_label_id()
            store_pointer = self._get_store_id()
        else:
            store_pointer = Unpacker._unpack_label()
        value = Packer.pack_label(store_pointer,label)
        self._write_bytes(self.labels,label.id,value)
        return label

    def write_property(self,property: Property) -> Property:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param property - property to write:
        """
        if property.id == INVALID_ID:
            property.id = self._get_property_id()
        if property.type == PropertyType.STRING:
            store_pointer = self._get_store_id()
            value = Packer.pack_property_store(store_pointer,property)
        else:
            value = Packer.pack_property(property)
        self._write_bytes(self.property,property.id,value)
        return property

    def write_relation(self,relation: Relationship) -> Relationship:
        """
        Writes relation to file.
        :param relation - relation written:
        """
        if relation.id == INVALID_ID:
            relation.id = self._get_relation_id()
        value = Packer.pack_relation(relation)
        self._write_bytes(self.relation,relation.id,value)
        return relation

    def write_store(self,value :str,pointer :int) -> int:
        """
        Writes values as dynamic store and returns pointer to first chunk of dynamic store
        :param value - string to write:
        """
        store = Packer.pack_value(pointer,value)
        self._write_bytes(self.store,pointer,store)
        return pointer

    def _write_bytes(self,file : _io.TextIOWrapper,pointer:int,data:bytes):
        """
        Writes data to file with given offset
        :param file: file object to write to
        :param pointer: offset
        :param data: bytes to write
        :return: None
        """
        file.seek(pointer)
        file.write(data)

    def read_node(self, id):
        """
        Reads single node by it's id
        :param id: offset of node to read
        :return: Node unpacked
        """
        node_bytes = self._read_bytes(self.nodes,id,cfg.NODE_SIZE)
        node = Unpacker.unpack_node(id,node_bytes)
        return node

    def read_label(self, id):
        """
        Reads single label by it's id
        :param id: offset of node to read
        :return: Node unpacked
        """
        label_bytes = self._read_bytes(self.labels, id, cfg.LABEL_SIZE)
        label = Unpacker.unpack_label(id,label_bytes)
        return label

    def read_property(self, id):
        """
        Reads single property by it's id
        :param id: offset of property to read
        :return: Property unpacked
        """
        property_bytes = self._read_bytes(self.properties, id, cfg.PROPERTY_SIZE)
        property = Unpacker.unpack_property(id,property_bytes)
        return property

    def read_relation(self, id):
        """
        Reads single relation by it's id
        :param id: offset of relation to read
        :return: Relation unpacked
        """
        relation_bytes = self._read_bytes(self.relations, id, cfg.RELATION_SIZE)
        relation = Unpacker.unpack_relation(id,relation_bytes)
        return relation

    def _read_bytes(self,file: _io.TextIOWrapper, offset : int, size: int) -> bytes:
        """
        Read chunks of bytes from filename specified by offset and size
        :param filename: to read from
        :param offset: starting location
        :param size: amount of bytes to read
        :return: bytes
        """
        file.seek(offset)
        return file.read(size)

    def _get_label_id(self) -> int:
        """
        Generates new pointer for label
        :return: pointer to label
        """
        self.last_label_id += 1
        return self.last_label_id

    def _get_node_id(self):
        """
        Generates new pointer for node
        :return: pointer to node
        """
        self.last_node_id += 1
        return self.last_node_id

    def _get_store_id(self):
        """
        Generates new pointer for store
        :return: pointer to store
        """
        self.last_store_id +=1
        return self.last_store_id

    def _get_property_id(self):
        """
        Generates new pointer for property
        :return: pointer to property
        """
        self.last_property_id +=1
        return self.last_property_id

    def _get_relation_id(self):
        self.last_relation_id +=1
        return self.last_relation_id

