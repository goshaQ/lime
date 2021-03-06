import sys
sys.path.append('')
from src.errors.WrongStatement import WrongStatement

"""
    This class parses queries with "CREATE" and "MATCH" clauses.
"""

class Parser():

    def __init__(self):
        pass

    def parse(self, query):
        """
        Parse the query

        :param query: A string with the query (in Cypher query language format)
        :return: list of nodes and list of edges with their properties
        """
        query = query.lower()
        tokens = query.split(" ")
        if "create" == tokens[0]:
            if "index" == tokens[1]:
                return self._create_index(tokens, query)
            else:
                return self._create_clause(tokens, query)
        elif "match" == tokens[0]:
            if "create" in query:
                return self._create_relationship(query)
            else:
                return self._match_query(tokens, query)
        elif "remove" == tokens[0]:
            return self._remove_clause(query)
        else:
            raise WrongStatement("RTFM")

    def _create_relationship(self, query):
        """
        MATCH (a:Figure {x: 10}), (b:Figure {x: 10, y:15})
        CREATE (a)-[r:LEFT {color: red}]->(b)
        RETURN a, b
        """
        label_first = query.split(":", 1)[1].split(")", 1)[0].replace(' ', '').split('{', 1)[0]
        label_second = query.split(",", 1)[1].split(":", 1)[1].split(")", 1)[0].replace(' ', '').split('{', 1)[0]

        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        properties_first = []
        for p in properties:
            properties_first.append(p.split(':', 1)[1])
        properties = query.split(',', 1)[1].split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        properties_second = []
        for p in properties:
            properties_second.append(p.split(':', 1)[1])

        direction = self._get_direction(query.split("create", 1)[1])
        
        rel_type = query.split('create', 1)[1].split(':', 1)[1].split(']', 1)[0].replace(' ', '')
        rel_prop = []
        if '{' in rel_type:
            properties = rel_type.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
            rel_type = rel_type.split('{', 1)[0]
            for p in properties:
                rel_prop.append(p.split(':', 1)[1])
        return [label_first, label_second], [properties_first, properties_second], direction, rel_type, rel_prop
        

    def _create_index(self, tokens, query):
        """
        'CREATE INDEX (ind:Index {<property>}) RETURN ind'
        """
        label = tokens[2].split(':', 1)[1]
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        values = []
        for p in properties:
            values.append(p.split(':', 1)[1])
        return label, values
            
    
    def _create_clause(self, tokens, query):
        """
        CREATE (node:Figure {x: 10, y: 15}) RETURN node
        """
        label = tokens[1].replace('(', '').split(':', 1)[1]
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        node_data = []
        types = []
        for p in properties:
            v = p.split(':', 1)[1]
            node_data.append(v)
            types.append(type(v))
        return label, node_data, types

    def _match_query(self, tokens, query):
        """
        MATCH (node:Figure {x: 10}) RETURN node
        """
        if "[:" in query:
            return self._match_by_relations(query)
        else:
            label = tokens[1].replace('(', '').split(':', 1)[1]
            return label, self._match_by_properties(query)

    def _match_by_relations(self, query):
        """
        A method for parsing query with relationships
        MATCH (node:Figure {x: 10, y:15})-[:LEFT]->(node1:Figure) RETURN node1
        MATCH (node:Figure {x:10, y:15})-[:LEFT {color: red}]->(node1:Figure) RETURN node1

        :return nodes, relationships: A tuples with nodes data and relations data
        """
        node_properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        node_label = query.split('(', 1)[1].split(')', 1)[0].replace(' ', '').split(':', 1)[1].split('{', 1)[0]
        node_values = []
        for p in node_properties:
            node_values.append(p.split(':', 1)[1])
        relations = [] # [direction, label, properties]
        while "[:" in query:
            relations.append(self._get_direction(query)) # A direction
            query = query.split('[:', 1)[1]
            relations.append(query.split(']', 1)[0].split(' ', 1)[0]) # A label
            label = query.split(':', 1)[0]
            if '{' in label:
                properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
                prop = []
                for p in properties:
                    prop.append(p.split(':', 1)[1])
                relations.append(prop)
        return node_label, node_values, relations
        

    def _get_direction(self, query):
        direction = query.split(')', 1)[1].split('(', 1)[0]
        first_part = direction.split('[', 1)[0]
        second_part = direction.split(']', 1)[1]
        direction = first_part + second_part
        if "-->" == direction:
            return 1
        elif "<--" == direction:
            return -1
        elif "--" == direction:
            return 0
        else:
            print("RTFM")

    def _match_by_properties(self, query):
        if '{' in query:
            properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
            values = []
            for p in properties:
                values.append(p.split(':', 1)[1])
            return values
        else:
            return []

    def _get_property_and_value(self, condition):
        prop = condition.split('.', 1)[1].split('=',1)[0]
        value = condition.split('=', 1)[1]
        return prop, value

    def _remove_clause(self, query):
        """
        REMOVE (node:Figure {x: 10, y:10}) RETURN node
        """
        label = query.split(':', 1)[1].replace(' ', '').split('{', 1)[0]
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        values = []
        for p in properties:
            values.append(p.split(':', 1)[1])
        return label, values