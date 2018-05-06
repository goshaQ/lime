from queryParser import Parser
from label import Label
from property import Property
from property_type import PropertyType
from graph_engine import GraphEngine
# from relationCreator import RelationCreator

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
        for i in range(1, len(properties) - 2):
            properties[i].next_prop(properties[i+1])
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
            for i in range(1, len(properties) - 2):
                properties[i].next_prop(properties[i+1])
            assert(len(node_data) == len(properties))
            self._engine.create_node((label, properties[0]))
            # Hardcoded:
            objects.append([node_data[0], node_data[1]])
        # self._create_relations(objects)
        
    def _create_relations(self, objects):
        # relationCreator = RelationCreator()
        pass

        

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
            node_label, node_values, relations = self._parser.parse(query)
            node_label = Label(self._id, node_label)
            properties = []
            for p in node_values:
                v = Property(self._id, PropertyType.STRING, node_label, p, None)
                properties.append(v)
            for i in range(1, len(properties) - 2):
                properties[i].next_prop(properties[i+1])
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
                for i in range(1, len(properties) - 2):
                    properties[i].next_prop(properties[i+1])
                assert(len(relations[2]) == len(properties))
                relationships.append((label, properties, direction))
            else:
                direction = relations[0]
                label = Label(self._id, relations[1])
                relationships.append((label, None, direction))

            self._engine.match_pattern(nodes, relationships)
        
# exec = Executor()
# query = "MATCH (node:Figure {x: 9, y: 10}) RETURN node"
# query = "MATCH (node1:Figure {x: 9, y:10})-[:LEFT {x:10, y: 0}]->(node2:Figure) RETURN node2"
# query = "CREATE INDEX (ind:Index {x: 10, y: 18}) RETURN ind"
# exec.execute_indexing(query)
# exec.execute_getting(query)