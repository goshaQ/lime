import sys
sys.path.append('')
from src.parser.queryExecutor import Executor
import json

class Interface():
    
    def __init__(self):
        self._executor = Executor()

    def add_index(self, query):
        return self._executor.execute_indexing(query)

    def add_figures(self, data):
        queries = []
        for d in data:
            x = round(d['x'], 2)
            y = round(d['y'], 2)
            query = "CREATE (node:Figure {x: %f, y: %f}) RETURN node" % (x, y)
            queries.append(query)
        return self._executor.execute_creation(queries)
    
    def add_figure(self, query):
        return self._executor.execute_creation([query])

    def add_relationship(self, query):
        return self._executor.add_relationship(query)

    def _check_existence(self, x, y):
        query = "MATCH (node:Figure {x: %f, y: %f} RETURN node)" % (x, y)
        nodes = self._executor.execute_getting(query, checkExistence=True)
        if nodes is not None:
            return True
        else:
            return False

    def get_figures(self, query):
        return self._executor.execute_getting(query)

    def remove_node(self, query):
        return self._executor.execute_removing(query)