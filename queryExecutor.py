from queryParser import Parser
from label import Label
from property import Property
from property_type import PropertyType
from graph_engine import GraphEngine
from types import *

class Executor():

    def __init__(self):
        self._parser = Parser()
        self._id = 1 # TODO; MIN_INT from config.py
        self._engine = GraphEngine()

    def execute_creation(self, queries):
        for query in queries:
            label, node_data, types = self._parser.parse(query)
            label = Label(self._id, label)
            properties = []
            for p in node_data:
                v = Property(self._id, PropertyType.STRING, label, p, None)
                properties.append(v)
            for i in range(1, len(properties) - 2):
                properties[i].next_prop(properties[i+1])
            assert(len(node_data) == len(properties))
            self._engine.create_node((label, properties[0]))

    def execute_getting(self, query, checkExistence=False):
        if checkExistence:
            label, data = self._parser.parse(query)
            label = Label(self._id, label)
            properties = []
            for p in data:
                v = Property(self._id, PropertyType.STRING, label, p, None)
                properties.append(v)
            for i in range(1, len(properties) - 2):
                properties[i].next_prop(properties[i+1])
            assert(len(data) == len(properties))
            return self._engine.match_pattern((label, properties), relationships=None)
        else:
            pass
        
# exec = Executor()
# query = "MATCH (node:Figure {x: 9, y: 10}) RETURN node"
# print(exec.execute_getting(query, True))