import sys
sys.path.append('')
import unittest
from src.parser.queryExecutor import Executor

class ExecutorTest():

    def setUP(self):
        self._executor = Executor()