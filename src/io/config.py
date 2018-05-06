import struct

STORE_SIZE = struct.calcsize("? i 24c")
NODE_SIZE = struct.calcsize("? i i i")
RELATION_SIZE = struct.calcsize("? ? i i i i i i i i")
PROPERTY_SIZE = struct.calcsize("? i i i i")
LABEL_SIZE = struct.calcsize("? i")

NODE_FILENAME = ""
LABEL_FILENAME = ""
PROPERTY_FILENAME = ""
STORE_FILANAME = ""
RELATION_FILENAME = ""