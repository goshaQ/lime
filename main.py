from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.io.packer import Packer
from src.io.unpacker import Unpacker
from src.io.io import Io
import unittest
import src.config as config

class TestIO(unittest.TestCase):

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


    def test_string_property_io(self):
        io = Io()
        value = "I LOVE ADB"
        label = Label(config.INV_ID,value)
        label = io.write_label(label)
        property = Property(config.INV_ID,PropertyType.STRING,label,value,config.INV_ID)
        written = io.write_property(property)
        retrieved = io.read_property(written.id)
        self.assertEqual(property.id,retrieved.id)
        self.assertEqual(property.value,retrieved.value)
        self.assertEqual(property.type.value,retrieved.type.value)
        self.assertEqual(property.label.value,retrieved.label.value)
        self.assertEqual(property.next_prop,retrieved.next_prop)

if __name__ == '__main__':

    unittest.main()