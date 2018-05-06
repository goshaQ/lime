from src.engine.label import Label
from src.engine.node import Node
from src.io.packer import Packer
from src.io.unpacker import Unpacker
from src.io.io import Io
import unittest
import src.config as config

class TestPacking(unittest.TestCase):

    def test_store_io(self):
        io = Io()
        store = "ADB is THE BEST COURSE"
        pointer = io.write_store(store)
        retrieved = io.read_store(pointer)
        self.assertEqual(store,retrieved)

    def test_label_io(self):
        io = Io()
        value = "I LOVE ADB"
        label = Label(config.INV_ID,value)
        written = io.write_label(label)
        retrieved = io.read_label(written.id)
        self.assertEqual(label.id,retrieved.id)
        self.assertEqual(label.value,retrieved.value)

if __name__ == '__main__':

    unittest.main()