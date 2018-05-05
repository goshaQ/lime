from queryParser import Parser

def add_figures():
    parser = Parser()
    # TODO: read from UDP
    data = None
    # TODO: create query with data
    query = "CREATE (node:Figure {%s}) RETURN node" % (data)
    label, node_data = parser.parse(query)
    

def get_figures():
    pass