import time
import unittest
import config as cfg

from src.engine.graph_engine import GraphEngine
from src.engine.label import Label
from src.engine.property import Property
from src.engine.property_type import PropertyType


class TestGraphEngine(unittest.TestCase):

    def test_create_node(self):
        engine = GraphEngine()

        label1 = Label(cfg.INV_ID, 'Figure')
        label2 = Label(cfg.INV_ID, 'x')
        label3 = Label(cfg.INV_ID, 'y')

        property2 = Property(cfg.INV_ID, PropertyType.INT, label2, 7, None)
        property1 = Property(cfg.INV_ID, PropertyType.INT, label3, 7, property2)

        engine.create_node((label1, property1))
        retrieved_node1 = engine.match_pattern(list((label1, property1)), None).pop()

        self.assertEqual(label1.value, retrieved_node1.label.value)
        self.assertEqual(property1.value, retrieved_node1.next_prop.value)
        self.assertEqual(property2.value, retrieved_node1.next_prop.next_prop.value)

    def test_create_relationship(self):
        engine = GraphEngine()

        label1 = Label(cfg.INV_ID, 'Figure')
        label2 = Label(cfg.INV_ID, 'x')
        label3 = Label(cfg.INV_ID, 'y')
        label4 = Label(cfg.INV_ID, 'Right')

        property2 = Property(cfg.INV_ID, PropertyType.INT, label2, 7, None)
        property1 = Property(cfg.INV_ID, PropertyType.INT, label3, 7, property2)
        property4 = Property(cfg.INV_ID, PropertyType.INT, label2, 6, None)
        property3 = Property(cfg.INV_ID, PropertyType.INT, label3, 6, property4)
        property6 = Property(cfg.INV_ID, PropertyType.INT, label2, 5, None)
        property5 = Property(cfg.INV_ID, PropertyType.INT, label3, 5, property6)

        engine.create_node((label1, property1))
        engine.create_node((label1, property3))
        engine.create_node((label1, property5))

        engine.create_relationship((label1, property1), (label1, property5), (label4, None, 1))
        retrieved_relationship = engine.match_pattern([(label1, property1), (label1, property5)], [(label4, None, 0)])

        start_node = retrieved_relationship[0].pop()
        end_node = retrieved_relationship[1].pop()
        self.assertEqual(start_node.label.value, label1.value)
        self.assertEqual(start_node.next_prop.value, property1.value)
        self.assertEqual(start_node.next_prop.next_prop.value, property2.value)
        self.assertEqual(end_node.label.value, label1.value)
        self.assertEqual(end_node.next_prop.value, property5.value)
        self.assertEqual(end_node.next_prop.next_prop.value, property6.value)

    def test_create_index(self):
        engine = GraphEngine()

        label1 = Label(cfg.INV_ID, 'Figure')
        label2 = Label(cfg.INV_ID, 'x')
        label3 = Label(cfg.INV_ID, 'y')

        limit = 1000
        property2 = property1 = None

        for idx in range(limit):
            property2 = Property(cfg.INV_ID, PropertyType.INT, label2, idx, None)
            property1 = Property(cfg.INV_ID, PropertyType.INT, label3, idx, property2)

            engine.create_node((label1, property1))

        start = time.time()
        retrieved_node1 = engine.match_pattern(list((label1, property1)), None).pop()
        end = time.time()
        time_no_index = end - start

        self.assertEqual(label1.value, retrieved_node1.label.value)
        self.assertEqual(property1.value, retrieved_node1.next_prop.value)
        self.assertEqual(property2.value, retrieved_node1.next_prop.next_prop.value)

        start = time.time()
        retrieved_node1 = engine.match_pattern(list((label1, property1)), None).pop()
        end = time.time()
        time_index = end - start

        self.assertEqual(label1.value, retrieved_node1.label.value)
        self.assertEqual(property1.value, retrieved_node1.next_prop.value)
        self.assertEqual(property2.value, retrieved_node1.next_prop.next_prop.value)

        self.assertLess(time_index, time_no_index)

if __name__ == '__main__':
unittest.main()