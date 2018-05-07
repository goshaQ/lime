import struct

STORE_SIZE = struct.calcsize("? i 24p")
NODE_SIZE = struct.calcsize("? i i i")
RELATION_SIZE = struct.calcsize("? ? i i i i i i i i")
PROPERTY_SIZE = struct.calcsize("? i i i i")
LABEL_SIZE = struct.calcsize("? i")

INV_ID = -2147483648


FILES_DIRECTORY = "store\\"
NODE_FILENAME = "nodes"
LABEL_FILENAME = "labels"
PROPERTY_FILENAME = "properties"
STORE_FILENAME = "store"
RELATIONSHIP_FILENAME = "relationships"
