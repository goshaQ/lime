import sys
sys.path.append('')

from queryParser import Parser
from src.engine.label import Label
from src.engine.property import Property
from src.engine.property_type import PropertyType
from src.engine.graph_engine import GraphEngine
from relationCreator import RelationCreator

class Executor():

    def __init__(self):
        self._parser = Parser()
        self._id = 1 # TODO; MIN_INT from config.py
        self._engine = GraphEngine()

    def execute_indexing(self, query):
        label, values = self._parser.parse(query)
        label = Label(self._id, label)
        properties = []
        for p in values:
            v = Property(self._id, PropertyType.STRING, label, p, None)
            properties.append(v)
        for i in range(len(properties) - 2):
            properties[i].next_prop = properties[i+1]
        assert(len(values) == len(properties))
        # TODO: send to indexing in engine

    def execute_creation(self, queries):
        objects = []
        for query in queries:
            label, node_data, types = self._parser.parse(query)
            label = Label(self._id, label)
            properties = []
            for p in node_data:
                v = Property(self._id, PropertyType.STRING, label, p, None)
                properties.append(v)
            for i in range(len(properties) - 2):
                properties[i].next_prop = properties[i+1]
            assert(len(node_data) == len(properties))
            self._engine.create_node((label, properties[0]))
            objects.append([label, properties[0]])
        self._create_relations(objects)
        
    def _create_relations(self, objects):
        relationCreator = RelationCreator()
        relationCreator.add_objects(objects) 
        for obj in objects:
            left, right, up, down = relationCreator.get_relations(obj) # left = [label, properties[0]]
            if None != left:
                self._engine.create_relationship((obj[0], obj[1]), (left[0], left[1]), (Label(self._id, 'left'), None, 1))
            if None != right:
                self._engine.create_relationship((obj[0], obj[1]), (right[0], right[1]), (Label(self._id, 'right'), None, 1))
            if None != up:    
                self._engine.create_relationship((obj[0], obj[1]), (up[0], up[1]), (Label(self._id, 'up'), None, 1))
            if None != down:
                self._engine.create_relationship((obj[0], obj[1]), (down[0], down[1]), (Label(self._id, 'down'), None, 1))

        
    def execute_getting(self, query, checkExistence=False):
        if checkExistence:
            label, data = self._parser.parse(query)
            label = Label(self._id, label)
            properties = []
            for p in data:
                v = Property(self._id, PropertyType.STRING, label, p, None)
                properties.append(v)
            for i in range(len(properties) - 2):
                properties[i].next_prop = properties[i+1]
            assert(len(data) == len(properties))
            return self._engine.match_pattern((label, properties), relationships=None)
        else:
            node_label, node_values, relations = self._parser.parse(query)
            node_label = Label(self._id, node_label)
            properties = []
            for p in node_values:
                v = Property(self._id, PropertyType.STRING, node_label, p, None)
                properties.append(v)
            for i in range(len(properties) - 2):
                properties[i].next_prop = properties[i+1]
            assert(len(node_values) == len(properties))
            nodes = [(node_label, properties)]
            relationships = []
            if len(relations) > 2:
                direction = relations[0]
                label = Label(self._id, relations[1])
                properties = []
                for p in relations[2]:
                    v = Property(self._id, PropertyType.STRING, label, p, None)
                    properties.append(v)
                for i in range(len(properties) - 2):
                    properties[i].next_prop = properties[i+1]
                assert(len(relations[2]) == len(properties))
                relationships.append((label, properties, direction))
            else:
                direction = relations[0]
                label = Label(self._id, relations[1])
                relationships.append((label, None, direction))

            self._engine.match_pattern(nodes, relationships)

    def execute_removing(self, query):
        label, values = self._parser.parse(query)
        label = Label(self._id, label)
        properties = []
        for p in values:
            v = Property(self._id, PropertyType.STRING, label, p, None)
            properties.append(v)
        for i in range(len(properties) - 2):
            properties[i].next_prop = properties[i+1]
        assert(len(values) == len(properties))
        self._engine.delete_node((label, properties))