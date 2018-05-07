import sys
sys.path.append('')
import unittest
from src.parser.queryParser import Parser
from src.errors.WrongStatement import WrongStatement

class ParserTest(unittest.TestCase):

    def setUp(self):
        self._parser = Parser()

    def testRTFM(self):
        query = "DROP (node:Figure {x: 10, y:10}) RETURN node"
        with self.assertRaises(WrongStatement) as context:
            self._parser.parse(query)

        self.assertTrue('RTFM' in str(context.exception))
        
    def testCreateA(self):
        query = "CREATE (node:Figure {x: 10, y: 15, color: red}) RETURN node"
        label, data, types = self._parser.parse(query)
        self.assertTrue(label == "figure")
        self.assertTrue('10' == data[0])
        self.assertTrue('15' == data[1])

    def testCreateIndex1(self):
        query = "CREATE (ind:Index {x: 10}) RETURN ind"
        try :
            label, values = self._parser.parse(query)
            self.assertTrue("index" == label)
            self.assertTrue("10" == values[0])
        except Exception as e:
            self.assertTrue("too many values to unpack (expected 2)" in str(e))

    def testCreateIndex2(self):
        query = "CREATE INDEX (ind:Index {x: 10}) RETURN ind"
        label, values = self._parser.parse(query)
        self.assertTrue("index" == label)
        self.assertTrue("10" == values[0])

    def testMatch(self):
        query = "MATCH (node:Figure {x: 10, y: 16}) RETURN node"
        label, values = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue("10" == values[0])
        self.assertTrue("16" == values[1])

    def testMatchWithRelation1(self):
        query = "MATCH (node1:Figure {x: 10, y: 19})-[:LEFT]->(node2:Figure) RETURN node2"
        label, values, relations = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue('10' == values[0])
        self.assertTrue('19' == values[1])
        self.assertTrue(1 == relations[0])
        self.assertTrue('left' == relations[1])

    def testMatchWithRelation2(self):
        query = "MATCH (node1:Figure {x: 10, y: 19})-[:LEFT {x: 14}]->(node2:Figure) RETURN node2"
        label, values, relations = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue('10' == values[0])
        self.assertTrue('19' == values[1])
        self.assertTrue(1 == relations[0])
        self.assertTrue('left' == relations[1])
        self.assertTrue('14' == relations[2][0])

    def testMatchWithRelation3(self):
        query = "MATCH (node1:Figure {x: 10, y: 19})-[:LEFT {x: 14, color: red}]->(node2:Figure) RETURN node2"
        label, values, relations = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue('10' == values[0])
        self.assertTrue('19' == values[1])
        self.assertTrue(1 == relations[0])
        self.assertTrue('left' == relations[1])
        self.assertTrue('14' == relations[2][0])
        self.assertTrue('red' == relations[2][1])

    def testMatchWithRelation4(self):
        query = "MATCH (node1:Figure {x: 10, y: 19})<-[:LEFT {x: 14}]-(node2:Figure) RETURN node2"
        label, values, relations = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue('10' == values[0])
        self.assertTrue('19' == values[1])
        self.assertTrue(-1 == relations[0])
        self.assertTrue('left' == relations[1])
        self.assertTrue('14' == relations[2][0])
    
    def testMatchWithRelation5(self):
        query = "MATCH (node1:Figure {x: 10, y: 19})-[:LEFT {x: 14}]-(node2:Figure) RETURN node2"
        label, values, relations = self._parser.parse(query)
        self.assertTrue("figure" == label)
        self.assertTrue('10' == values[0])
        self.assertTrue('19' == values[1])
        self.assertTrue(0 == relations[0])
        self.assertTrue('left' == relations[1])
        self.assertTrue('14' == relations[2][0])

    def testMatchWithRelation6(self):
        query = "MATCH (a:Figure {x: 10}), (b:Figure {x: 10, y:15}) CREATE (a)-[r:LEFT {color: red}]->(b) RETURN a, b"
        labels, properties, direction, rel_type, rel_props = self._parser.parse(query)
        self.assertTrue('figure' == labels[0])
        self.assertTrue('figure' == labels[1])
        self.assertTrue('10' == properties[0][0])
        self.assertTrue('10' == properties[1][0])
        self.assertTrue('15' == properties[1][1])
        self.assertTrue(1 == direction)
        self.assertTrue('left' == rel_type)
        self.assertTrue('red' == rel_props[0])
        

if __name__ == "__main__":
    unittest.main()