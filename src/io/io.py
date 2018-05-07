import os
import _io
import config as cfg

from engine.label import Label
from engine.node import Node
from engine.property import Property
from engine.property_type import PropertyType
from engine.relationship import Relationship

from io.packer import Packer
from io.unpacker import Unpacker


class Io:

    def __init__(self,):
        self.nodes = open(cfg.NODE_FILENAME,"a+b")
        self.labels = open(cfg.LABEL_FILENAME,"a+b")
        self.properties = open(cfg.PROPERTY_FILENAME,"a+b")
        self.relations = open(cfg.RELATION_FILENAME,"a+b")
        self.store = open(cfg.STORE_FILANAME,"a+b")
        self.last_node_id = int(os.stat(cfg.NODE_FILENAME).st_size / cfg.NODE_SIZE)
        self.last_relation_id = int(os.stat(cfg.RELATION_FILENAME).st_size / cfg.RELATION_SIZE)
        self.last_property_id = int(os.stat(cfg.PROPERTY_FILENAME).st_size / cfg.PROPERTY_SIZE)
        self.last_label_id = int(os.stat(cfg.LABEL_FILENAME).st_size / cfg.LABEL_SIZE)
        self.last_store_id = int(os.stat(cfg.STORE_FILANAME).st_size / cfg.STORE_SIZE)

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
            node = self.read_node(id)
            if node != cfg.INV_ID:
                result.append(node)
        return result

    def get_labels_by_id(self, labels: set) -> list:
        """
        Gets labels by specified id. If input set is empty fetches all labels
        :param labels: - set of id's to fetch
        :return: list of labels with matching id
        """
        if len(labels) == 0:
            labels = range(0,self.last_label_id,cfg.LABEL_SIZE)
        result = []
        for id in labels:
            label = self.read_label(id)
            if label != cfg.INV_ID:
                result.append(label)
        return result

    def get_relations_by_id(self, relations: set) -> list:
        """
        Gets relations by specified id. If input set is empty fetches all relations
        :param relations: - set of id's to fetch
        :return: list of relations with matching id
        """
        if len(relations) == 0:
            relations = range(0,self.last_relation_id,cfg.RELATION_SIZE)
        result = []
        for id in relations:
            relation = self.read_relation(id)
            if relation != cfg.INV_ID:
                result.append(relation)
        return result

    def write_node(self, node: Node) -> Node:
        """
        Writes node to file.
        :param node to pack:
        :return: byte represenation of string
        """
        if node.id == cfg.INV_ID:
            node.id = self._get_node_id()
        value = Packer.pack_node(node)
        node.label = self.write_label(node.label)
        if node.next_prop != config.INV_ID:
            node.next_prop = self.write_property(node.next_prop)
        self._write_bytes(self.nodes,node.id*cfg.NODE_SIZE,value)
        return node

    def write_label(self,label: Label) -> Label:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param property - property to write:
        """
        if label.id == cfg.INV_ID:
            label.id = self._get_label_id()
        store_pointer = self.write_store(label.value)
        value = Packer.pack_label(store_pointer,label)
        self._write_bytes(self.labels,label.id*cfg.LABEL_SIZE,value)
        return label

    def write_property(self,property: Property) -> Property:
        """
        Writes property to file. Creates dynamic store if needed by property type. Inlines otherwise.
        :param property - property to write:
        """
        if property.id == cfg.INV_ID:
            property.id = self._get_property_id()
        if property.type.value == PropertyType.STRING.value:
            store_pointer = self.write_store(property.value)
            value = Packer.pack_property_store(store_pointer,property)
        else:
            value = Packer.pack_property_inline(property)
        self._write_bytes(self.properties,property.id*cfg.PROPERTY_SIZE,value)
        return property

    def write_relation(self,relation: Relationship) -> Relationship:
        """
        Writes relation to file.
        :param relation - relation written:
        """
        if relation.id == cfg.INV_ID:
            relation.id = self._get_relation_id()
        value = Packer.pack_relation(relation)
        label = self.write_label(relation.label)
        property = self.write_property(relation.next_prop)

        self._write_bytes(self.relations,relation.id*cfg.RELATION_SIZE,value)
        return relation

    def write_store(self,value :str) -> int:
        """
        Writes values as dynamic store and returns pointer to first chunk of dynamic store
        :param value - string to write:
        """
        first_pointer = self._get_store_id()
        pointer = first_pointer
        for i in range(0, len(value)-24, 24):
            next_pointer = self._get_store_id()
            store = Packer.pack_value(next_pointer,value[:24])
            value = value[23:]
            self._write_bytes(self.store,pointer,store)
            pointer = next_pointer
        next_pointer = cfg.INV_ID
        store = Packer.pack_value(next_pointer, value[:24])
        self._write_bytes(self.store, pointer, store)
        return first_pointer

    def _write_bytes(self,file,pointer:int,data:bytes):
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
        if id>self.last_node_id:
            raise Exception('Property ID is out of range')
        node_bytes = self._read_bytes(self.nodes,id,cfg.NODE_SIZE)
        in_use,label_id, prop_id, relation_id = Unpacker.unpack_node(id,node_bytes)
        if in_use:
            label = self.read_label(label_id)
            return Node(id,label,prop_id,relation_id)
        else:
            return cfg.INV_ID

    def read_label(self, id) -> Label:
        """
        Reads single label by it's id
        :param id: offset of label to read
        :return: Label unpacked
        """
        if id>self.last_label_id:
            raise Exception('Label ID is out of range')

        label_bytes = self._read_bytes(self.labels, id, cfg.LABEL_SIZE)

        in_use,store_id = Unpacker.unpack_label(label_bytes)
        if in_use:
            value = self.read_store(store_id)
            return Label(id,value)
        else:
            return cfg.INV_ID

    def read_property(self, id: int) -> Property:
        """
        Reads single property by it's id
        :param id: offset of property to read
        :return: Property unpacked
        """
        if id>self.last_property_id:
            raise Exception('Property ID is out of range')
        property_bytes = self._read_bytes(self.properties, id, cfg.PROPERTY_SIZE)
        in_use,type, label_id, value, next_property_id = Unpacker.unpack_property(property_bytes)
        if type == PropertyType.STRING.value:
            value = self.read_store(value)
        if type == PropertyType.FLOAT.value:
            value = float(value)
        if type == PropertyType.CHAR.value:
            value = value.decode("utf8")
        if in_use:
            label = self.read_label(label_id)
            return Property(id,PropertyType(type),label,value,next_property_id)
        else:
            return cfg.INV_ID

    def read_relation(self, id) -> Relationship:
        """
        Reads single relation by it's id
        :param id: offset of relation to read
        :return: Relation unpacked
        """
        if id > self.last_relation_id:
            raise Exception('Relation ID is out of range')

        relation_bytes = self._read_bytes(self.relations, id, cfg.RELATION_SIZE)
        in_use,type, first_node, second_node, label, property, first_prev_relation, first_next_relation, second_prev_relation, second_next_realtion = Unpacker.unpack_relation(id,relation_bytes)
        if in_use:
            label = self.read_label(label)

            return Relationship(id, type, first_node, second_node, label, property,
                                first_prev_relation, first_next_relation, second_prev_relation, second_next_realtion)
        else:
            return cfg.INV_ID

    def read_store(self,id: int) -> str:
        """
        Reads single string from store
        :param id: id of first store block
        :return: string
        """
        value = b""
        if id>self.last_store_id:
            raise Exception('Id is out of range')
        while(id != config.INV_ID):
            store_bytes = self._read_bytes(self.store,id,cfg.STORE_SIZE)
            id,chunk = Unpacker.unpack_store(store_bytes)
            value += chunk
        return value.decode("utf8")

    def _read_bytes(self,file: _io.FileIO, offset : int, size: int) -> bytes:
        """
        Read chunks of bytes from filename specified by offset and size
        :param filename: to read from
        :param offset: starting location
        :param size: amount of bytes to read
        :return: bytes
        """
        file.seek(offset*size)
        return file.read(size)

    def del_node(self,id:int):
        """
        Delets node and all corresponding properties and relatins
        :param id: id to delete
        :return: None
        """
        node = self.read_node(id)
        new_bytes = Packer.pack_node(node,in_use=False)
        self._write_bytes(self.nodes,id*cfg.NODE_SIZE,new_bytes)
        self.del_property(node.next_prop)
        self.del_relation(node.next_rel)

    def del_relation(self,id:int):
        relation = self.read_relation(id)
        new_bytes = Packer.pack_relation(relation,in_use=False)
        self._write_bytes(self.relations,id*cfg.RELATION_SIZE,new_bytes)
        self.del_property(relation.next_prop)
        if relation.next_prop != config.INV_ID:
            self.del_property(relation.next_prop)
        if (relation.second_next_rel != config.INV_ID) and (relation.second_prev_rel != config.INV_ID):
            second_next_rel = self.read_relation(relation.second_next_rel)
            second_prev_rel = self.read_relation(relation.second_prev_rel)
            self._swap_relation_pointer(second_next_rel,second_prev_rel)

        elif (relation.second_next_rel != config.INV_ID) and not (relation.second_prev_rel != config.INV_ID):
            second_next_rel = self.read_relation(relation.second_next_rel)
            self._fix_next_rel(relation,second_next_rel)

        elif (relation.second_prev_rel != config.INV_ID) and not (relation.second_next_rel != config.INV_ID):
            second_prev_rel = self.read_relation(relation.second_prev_rel)
            self._fix_prev_rel(relation,second_prev_rel)

        if (relation.first_next_rel != config.INV_ID) and (relation.first_prev_rel != config.INV_ID):
            first_next_rel = self.read_relation(relation.first_next_rel)
            first_prev_rel = self.read_relation(relation.first_prev_rel)
            self._swap_relation_pointer(first_next_rel,first_prev_rel)

        elif (relation.first_next_rel != config.INV_ID) and not (relation.first_prev_rel != config.INV_ID):
            first_next_rel = self.read_relation(relation.first_next_rel)
            self._fix_next_rel(relation,first_next_rel)

        elif (relation.first_prev_rel != config.INV_ID) and not (relation.first_next_rel != config.INV_ID):
            first_prev_rel = self.read_relation(relation.first_prev_rel)
            self._fix_prev_rel(relation,first_prev_rel)

        node2 = self.read_node(relation.second_node)
        node1 = self.read_node(relation.first_node)
        self._fix_node_rel(relation, node1)
        self._fix_node_rel(relation, node2)

    def _fix_node_rel(self,current: Relationship,node:Node):
        if node.id == current.first_node:
            if node.next_rel == current.id:
                node.next_rel = current.first_next_rel
        if node.id == current.second_node:
            if node.next_rel == current.id:
                node.next_rel = current.second_next_rel
        self.write_node(node)

    def _fix_next_rel(self,current: Relationship,next_rel: Relationship):
        """
        Sets next_rel prev pointer to INV_ID
        :param current:
        :param next_rel:
        :return:
        """
        if(current.second_node == next_rel.second_node):
            next_rel.second_prev_id = config.INV_ID
        elif(current.second_node == next_rel.first_node):
            next_rel.first_prev_id = config.INV_ID
        prev_packed = Packer.pack_relation(next_rel)
        self._write_bytes(self.relations, next_rel.id, prev_packed)

    def _fix_prev_rel(self,current: Relationship,prev_rel: Relationship):
        """
        Sets prev_rel next pointer to INV_ID
        :param current:
        :param prev_rel:
        :return:
        """
        if(current.second_node == prev_rel.second_node):
            prev_rel.second_next_id = config.INV_ID
        elif(current.second_node == prev_rel.first_node):
            prev_rel.first_next_id = config.INV_ID
        prev_packed = Packer.pack_relation(prev_rel)
        self._write_bytes(self.relations, prev_rel.id, prev_packed)

    def _swap_relation_pointer(self,next: Relationship, prev: Relationship):
        """
        Swaps pointer of two relations. Helper function for deletion of relation
        :param next:
        :param prev:
        :return:
        """
        if (prev.second_node == next.second_node):
            prev.second_next_rel = next.id
            next.second_prev_rel = prev.id
        elif (prev.first_node == next.first_node):
            prev.first_next_rel = next.id
            next.first_prev_rel = prev.id
        elif (prev.first_node == next.second_node):
            prev.first_next_rel = next.id
            next.second_prev_rel = prev.id
        elif (prev.second_node == next.first_node):
            prev.second_next_rel = next.id
            next.first_prev_rel = prev.id
        else:
            raise Exception('No same nodes to swap')

        second_prev_rel_packed = Packer.pack_relation(prev)
        second_next_rel_packed = Packer.pack_relation(next)
        self._write_bytes(self.relations, next.id, second_next_rel_packed)
        self._write_bytes(self.relations, prev.id, second_prev_rel_packed)

    def del_property(self,id:int):
        """
        Marks signle property as unsued
        :param id:
        :return:
        """
        property = self.read_property(id)
        if property.type == PropertyType.STRING:
            new_bytes = Packer.pack_property_store(property,in_use=False)
        else:
            new_bytes = Packer.pack_property_inline(property,in_use=False)
        if property.next_prop != config.INV_ID:
            self.del_property(property.next_prop)
        self._write_bytes(self.properties,id*cfg.PROPERTY_SIZE,new_bytes)

    def del_store(self,id:int):
        """
        Marks single string as unused
        :param id:
        :return:
        """
        id,value = Unpacker.unpack_store(self._read_bytes(self.store,id,cfg.STORE_SIZE))
        if id != config.INV_ID:
            self.del_store(id)
        new_bytes = Packer.pack_value(id,value,in_use=False)
        self._write_bytes(self.store,id*cfg.STORE_SIZE,new_bytes)

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
        self.last_store_id +=1
        return pointer

    def _get_property_id(self):
        """
        Generates new pointer for property
        :return: pointer to property
        """
        pointer = self.last_property_id
        self.last_property_id +=1
        return pointer

    def _get_relation_id(self) -> int:
        pointer = self.last_relation_id
        self.last_relation_id +=1
        return pointer

