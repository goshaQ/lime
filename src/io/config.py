import struct

STORE_SIZE = struct.calcsize("? i 24p")
NODE_SIZE = struct.calcsize("? i i i")
RELATION_SIZE = struct.calcsize("? ? i i i i i i i i")
PROPERTY_SIZE = struct.calcsize("? i i i i")
LABEL_SIZE = struct.calcsize("? i")

NODE_FILENAME = "nodes"
LABEL_FILENAME = "labels"
PROPERTY_FILENAME = "properties"
STORE_FILANAME = "store"
RELATION_FILENAME = "relations"