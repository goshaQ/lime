import struct

import _io

from src.engine import node,relationship,label,property,property_type


STORE_SIZE = struct.calcsize("? i 24c")
NODE_SIZE = struct.calcsize("? i i i")
RELATION_SIZE = struct.calcsize("? i i ? i i i i i")
PROPERTY_SIZE = struct.calcsize("? i i i i")
LABEL_SIZE = struct.calcsize("? i")

class Io:
    def _create_writer(self):
        """
        Creates new instance of Writer class
        :return: object of type Writer
        """
        return Io.Writer(self)

    def _create_reader(self):
        """
        Creates new instance of Reader class
        :return: object of type Reader
        """
        return Io.Reader(self)

    def __init__(self,node_filename: str,label_filename: str,property_filename:str,store_filaname:str,relation_filename:str):
        self.nodes = open(node_filename,"rwb")
        self.labels = open(label_filename,"rwb")
        self.properties = open(property_filename,"rwb")
        self.relations = open(relation_filename,"rwb")
        self.store = open(store_filaname,"rwb")
        self.writer = self._create_writer()
        self.reader = self._create_reader()


    class Writer(object):
        def __init__(self,io):
            self.io = io

        def write_node(self, node: Node) -> bytes:
            """
            Packs node into byte struct format ready to write.
            :param node to pack:
            :return: byte represenation of string
            """
            label_pointer = _get_label_pointer(node.label)
            property_pointer = _get_property_pointer()
            relation_pointer = _get_relation_pointer()
            return struct.pack("? I I I",True, label_pointer,property_pointer,relation_pointer)

        def pack_label(self,label: Label) -> bytes:
            in_use = True
            value = _get_store_pointer()
            self.write_store(label.value)
            repr = struct.pack("?",in_use,value)
            return repr

        def pack_property(self,property: Property) -> str:
            pass

        def pack_relationship(self,relationship: Relationship) -> str:
            pass

        def write_store(self,value :str,pointer :int):
            """
            Writes values as dynamic store and returns pointer to first chunk of dynamic store
            :param value - string to write:
            """
            store = self._pack_value(value)
            self._write_bytes(self.io.store,self.io.last_store,self.io.store)

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

        def _pack_value(self, value: str) -> str:
            """
            Packs a string into Dynamic_Store format
            Divides input string into chunks 24 bytes (adds padding if len(value)<24)
            :return: concatenated Dynamic_store formatted bytes
            """
            blocks = b""
            for i in range(0,len(value),24):
                next_pointer = self._get_new_store_pointer()
                in_use = True
                data = bytes(value[i:i+24], encoding = "utf8")
                blocks = blocks + struct.pack("? i 24p",in_use,next_pointer,data)
            return blocks

        def _get_label_pointer(self,label : Label) -> int:
            """
            Searches for given label in our files. If no such label exists - points to empty region.
            :return: pointer to label
            """
            pointer = _get_pointer_by_label(label)
            if pointer:
                return pointer
            else:
                self.last_label = self.last_label+1
                pointer = self.last_label
                return pointer

        def _get_new_store_pointer(self) -> int:
            """
            Gets pointer to next free block in store file
            :return: pointer
            """
            self.io.last_store = self.io.last_store + 1
            return self.io.last_store

    class Reader:
        def __init__(self,io):
            self.io = io

        def unpack_node(node: bytes) -> Node:
            pass

        def _unpack_store(store : bytes) -> str:
            """
            Gets value from single Dynamic_Store byte
            :return:
            """
            value = b""
            for i in range(0,len(store),struct.calcsize("?i24p")):
                unpacked = struct.unpack("?i24p", store[i:i+STORE_SIZE])
                value += unpacked[2]
            return value.decode("utf8")


        def _read_bytes(filename: str, offset : int, size: int):
            file = open(filename)
            file.seek(offset)
            return file.read(size)
