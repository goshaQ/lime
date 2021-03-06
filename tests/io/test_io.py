import src.config as cfg
import unittest

from src.engine.label import Label
from src.engine.node import Node
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.relationship import Relationship
from src.io.io import Io
from src.io.packer import Packer
from src.io.unpacker import Unpacker


class TestIO(unittest.TestCase):

    def test_store_io(self):
        io = Io()
        store = "ADB is THE BEST COURSE"
        pointer = io.write_store(store)
        retrieved = io.read_store(pointer)
        self.assertEqual(store,retrieved)

    def test_big_store_io(self):
        io = Io()
        store = "ADB is THE BEST COURSE in the entire Innopolis University"
        pointer = io.write_store(store)
        retrieved = io.read_store(pointer)
        self.assertEqual(store,retrieved)

    def test_label_io(self):
        io = Io()
        value = "I LOVE ADB"
        label = Label(cfg.INV_ID, value)
        written = io.write_label(label)
        retrieved = io.read_label(written.id)
        self.assertEqual(label.id,retrieved.id)
        self.assertEqual(label.value,retrieved.value)

    def test_string_property_io(self):
        io = Io()
        value = "I LOVE ADB"
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        property = Property(cfg.INV_ID, PropertyType.STRING, label, value, None)
        written = io.write_property(property)
        retrieved = io.read_property(written.id)
        self.assertEqual(property.id,retrieved.id)
        self.assertEqual(property.value,retrieved.value)
        self.assertEqual(property.type.value,retrieved.type.value)
        self.assertEqual(property.label.value,retrieved.label.value)
        self.assertEqual(property.next_prop,retrieved.next_prop)

    def test_bool_property_io(self):
        io = Io()
        value = "I LOVE ADB"
        prop_value = True
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        written = io.write_property(property)
        retrieved = io.read_property(written.id)
        self.assertEqual(property.id,retrieved.id)
        self.assertEqual(property.value,retrieved.value)
        self.assertEqual(property.type.value,retrieved.type.value)
        self.assertEqual(property.label.value,retrieved.label.value)
        self.assertEqual(property.next_prop,retrieved.next_prop)

    def test_float_property_io(self):
        io = Io()
        value = "I LOVE ADB"
        prop_value = 0.5
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        property = Property(cfg.INV_ID, PropertyType.FLOAT, label, prop_value, None)
        written = io.write_property(property)
        retrieved = io.read_property(written.id)
        self.assertEqual(property.id,retrieved.id)
        self.assertEqual(property.value,retrieved.value)
        self.assertEqual(property.type.value,retrieved.type.value)
        self.assertEqual(property.label.value,retrieved.label.value)
        self.assertEqual(property.next_prop,retrieved.next_prop)

    def test_int_property_io(self):
        io = Io()
        value3 = "I LOVE ADB3"
        value2 = "I LOVE ADB2"
        value1 = "I LOVE ADB1"

        prop_value = 1
        label3 = Label(cfg.INV_ID, value3)
        label2 = Label(cfg.INV_ID, value2)
        label1 = Label(cfg.INV_ID, value1)

        property = Property(cfg.INV_ID, PropertyType.INT, label1, 1,None)
        property2 = Property(cfg.INV_ID, PropertyType.INT, label2, 2,property)
        property3 = Property(cfg.INV_ID, PropertyType.INT, label3, 3,property2)

        written = io.write_property(property3)
        retrieved = io.read_property(written.id)
        self.assertEqual(property3.id,retrieved.id)
        self.assertEqual(property3.value,retrieved.value)
        self.assertEqual(property3.type.value,retrieved.type.value)
        self.assertEqual(property3.label.value,retrieved.label.value)
        self.assertEqual(property3.next_prop.id,retrieved.next_prop.id)

    def test_node_io(self):
        io = Io()
        value = "Graph DB is AWESOME"
        label = Label(cfg.INV_ID, value)
        prop_value = True
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        node = Node(cfg.INV_ID, label, property, cfg.INV_ID)
        written = io.write_node(node)
        retrived = io.read_node(written.id)
        self.assertEqual(node.id,retrived.id)
        self.assertEqual(node.next_prop.id,retrived.next_prop.id)
        self.assertEqual(node.next_prop.label.value,property.label.value)
        self.assertEqual(node.label.value,retrived.label.value)
        self.assertEqual(node.label.id,retrived.label.id)

    def test_relation_io(self):
        io = Io()
        value = "You spin my head right ground right ground"
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        prop_value = True
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        property = io.write_property(property)
        node = Node(cfg.INV_ID, label, property, None)
        node2 = Node(cfg.INV_ID, label, property, None)
        written1 = io.write_node(node)
        written2 = io.write_node(node2)
        relation = Relationship(cfg.INV_ID, False, written1, written2, label, property, None, None, None, None)
        written = io.write_relation(relation)
        retrieved = io.read_relation(written.id)

        written1 = io.read_node(written1.id)
        written2 = io.read_node(written2.id)

        self.assertEqual(retrieved.label.value,value)
        self.assertEqual(retrieved.next_prop.value,prop_value)
        self.assertEqual(retrieved.first_node.id,written1.id)
        self.assertEqual(retrieved.second_node.id,written2.id)
        self.assertEqual(written2.next_rel,retrieved.id)
        self.assertEqual(written1.next_rel,retrieved.id)

    def test_del_relation(self):
        io = Io()
        value = "You spin my head right ground right ground"
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        prop_value = True
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        property = io.write_property(property)
        node = Node(cfg.INV_ID, label, property, None)
        node2 = Node(cfg.INV_ID, label, property, None)
        written1 = io.write_node(node)
        written2 = io.write_node(node2)
        relation = Relationship(cfg.INV_ID, False, written1, written2, label, property, None, None, None, None)
        written = io.write_relation(relation)
        io.del_relation(written.id)
        retrived = io.get_relations_by_id([written.id])
        node1 = io.read_node(written1.id)
        node2 = io.read_node(written2.id)
        self.assertEqual(len(retrived), 0)
        print(node1.next_rel)
        print(node2.next_rel)
        self.assertEqual(node1.next_rel is None,True)
        self.assertEqual(node2.next_rel is None, True)


    def test_node_deletion(self):
        io = Io()
        value = "Graph DB is AWESOME"
        label = Label(cfg.INV_ID, value)
        prop_value = True
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        node = Node(cfg.INV_ID, label, property, cfg.INV_ID)
        written = io.write_node(node)
        io.del_node(written.id)
        retrieved = io.get_nodes_by_id([written.id])
        self.assertEqual(len(retrieved), 0)

    def test_multirelation_deletion(self):
        io = Io()
        value = "You spin my head right ground right ground"
        label = Label(cfg.INV_ID, value)
        label = io.write_label(label)
        prop_value = True
        property = Property(cfg.INV_ID, PropertyType.BOOL, label, prop_value, None)
        property = io.write_property(property)
        node = Node(cfg.INV_ID, label, property, None)
        node2 = Node(cfg.INV_ID, label, property, None)
        written_node1 = io.write_node(node)
        written_node2 = io.write_node(node2)
        relation1 = Relationship(cfg.INV_ID, False, written_node1, written_node2, label, property, None, None, None, None)
        relation2 = Relationship(cfg.INV_ID, False, written_node1, written_node2, label, property, None, None, None, None)
        written_rel1 = io.write_relation(relation1)
        written_rel2 = io.write_relation(relation2)
        io.del_node(written_node1.id)
        retrived = io.get_relations_by_id([written_rel1.id,written_rel2.id])
        self.assertEqual(len(retrived),0)

    def test_get_nodes_io(self):
        io = Io()
        nodes = []
        for i in range(0,10):
            value = "Macarena"
            label = Label(cfg.INV_ID, value)
            label = io.write_label(label)
            node = Node(cfg.INV_ID, label, None, None)
            node = io.write_node(node)
            nodes.append(node.id)
        node_list = io.get_nodes_by_id(set(nodes))
        for id,node in enumerate(node_list):
            self.assertEqual(node.id,nodes[id])
            self.assertEqual(node.label.value,"Macarena")

if __name__ == '__main__':
    unittest.main()