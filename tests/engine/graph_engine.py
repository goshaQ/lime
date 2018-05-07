import config as cfg
import unittest

from engine.graph_engine import GraphEngine
from engine.label import Label
from engine.property import Property
from src.engine.property_type import PropertyType


class TestGraphEngine(unittest.TestCase):

    def test_create_node(self):
        engine = GraphEngine()

        label1 = Label(cfg.INV_ID, 'Figure')
        label2 = Label(cfg.INV_ID, 'x')
        label3 = Label(cfg.INV_ID, 'y')

        property2 = Property(cfg.INV_ID, PropertyType.INT, label2, 7, cfg.INV_ID)
        property1 = Property(cfg.INV_ID, PropertyType.STRING, label3, 7, property2)

        engine.create_node((label1, property1))
        retrieved_node1 = engine.match_pattern(list((label1, property1)), list()).pop()

        self.assertEqual(label1.value, retrieved_node1.label.value)
        self.assertEqual(property1.value, retrieved_node1.next_prop.value)
        self.assertEqual(property2, retrieved_node1.next_prop.next_prop.value)

if __name__ == '__main__':
    unittest.main()
