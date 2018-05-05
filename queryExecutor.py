from queryParser import Parser
from label import Label
from property import Property
from property_type import PropertyType
from graph_engine import GraphEngine

class Executor():

    def __init__(self):
        self._parser = Parser()
        self._id = 1
        self._engine = GraphEngine()

    def execute_creation(self, queries):
        for query in queries:
            label, node_data = self._parser.parse(query)
            label = Label(self._id, label)
            property_2 = Property(self._id, PropertyType.FLOAT, label, node_data[1], next_prop=None) # y
            property_1 = Property(self._id, PropertyType.FLOAT, label, node_data[0], property_2) # x
            self._engine.create_node((label, property_1))
            print("Gut")


    def execute_getting(self, queries):
        pass