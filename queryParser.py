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
                return self._create_index(query)
            else:
                return self._create_clause(tokens, query)
        elif "match" == tokens[0]:
            return self._match_query(query)
        else:
            print("Only 'CREATE' and 'MATCH' clauses are available")

    def _create_index(self, query):
        # TODO: implement
        pass
    
    def _create_clause(self, tokens, query):
        self._check_create(query)
        label = tokens[1].replace('(', '').split(':', 1)[1]
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',', 1)
        node_data = []
        for p in properties:
            node_data.append(p.split(':', 1)[1])
        return label, node_data
        

    def _check_create(self, query):
        # TODO: implement checking correctness of the query
        pass

    def _match_query(self, query):
        self._check_match(query)
        return self._match_by_properties(query)

    def _match_by_properties(self, query):
        properties = query.split('{', 1)[1].split('}', 1)[0].replace(' ', '').split(',')
        props = []
        values = []
        for p in properties:
            temp = p.split(':', 1)
            props.append(temp[0])
            values.append(temp[1])
        return [props, values]

    def _get_property_and_value(self, condition):
        prop = condition.split('.', 1)[1].split('=',1)[0]
        value = condition.split('=', 1)[1]
        return prop, value

    def _check_match(self, query):
        # TODO: implement checking correctness ofthe query
        pass





