from queryExecutor import Executor
import json

class Interface():
    
    def __init__(self):
        self._executor = Executor()

    def add_index(self):
        query = input("Enter query for index: ")
        self._executor.execute_indexing(query)

    def add_figures(self, data):
        queries = []
        for d in data:
            x = round(d['x'], 2)
            y = round(d['y'], 2)
            if not self._check_existence(x, y):
                query = "CREATE (node:Figure {x: %f, y: %f}) RETURN node" % (x, y)
                queries.append(query)
        self._executor.execute_creation(queries)

    def _check_existence(self, x, y):
        query = "MATCH (node:Figure {x: %f, y: %f} RETURN node)" % (x, y)
        nodes = self._executor.execute_getting(query, checkExistence=True)
        if 0 != len(nodes):
            return True
        else:
            return False

    def get_figures(self):
        query = input("Enter query: ")
        return self._executor.execute_getting(query)