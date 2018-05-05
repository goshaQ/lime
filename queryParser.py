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
            return self._create_clause(tokens, query)
        elif "match" == tokens[0]:
            pass
        else:
            print("Only 'CREATE' and 'MATCH' clauses are available")
    
    def _create_clause(self, tokens, query):
        self._check_create(tokens, query)
        label = tokens[1].replace('(', '').split(':', 1)[1]
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',', 1)
        node_data = []
        for p in properties:
            node_data.append(p.split(':', 1)[1])
        return label, node_data
        

    def _check_create(self, tokens, query):
        # TODO: implement checking correctness of the query
        pass

    def _match_query(self, tokens, query):
        self._check_match(tokens, query)


    def _check_match(self, tokens, query):
        # TODO: implement checking correctness ofthe query
        pass

parser = Parser()
query1 = "MATCH (node:Figure) RETURN node"
query2 = "MATCH (node1:Figure {color: green}) RETURN node"
query3 = "MATCH (node1:Figure)-[:BIGGER]->(node2:Figure) WHERE node1.x=10 RETURN node2"
query4 = "MATCH (node1:Figure)-[:BIGGER]->(node2:Figure) WHERE node1.x=10 AND node2.y=15 RETURN node2"





