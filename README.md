# lime

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing
```
git clone https://github.com/goshaQ/lime

cd lime/

pip3 install -r requirements.txt

python3 cli.py
```

## Work process
After running the `cli.py` two threads are created:
- Reading the data from UDP:
    - ip='127.0.0.1' 
    - port=9001
- Reading user queries

### User queries
- :help - if you want to read helper
- :node - if you want to add a new node
- :relationship - if you want to add a new relationship
- :index - if you want to add an index
- :remove - if you want to remove the node
- :search - if you want to search in the Database
- :quit - close the program

### Insert nodes
There are two possible ways for adding data to the database:
- Through UDP messages (mentioned before)
- Using SimpleCypherQL queries

If you want to add the node, type this skeleton:
```
CREATE (<nodeName>:<nodeLabel> {<properties>}) 
RETURN <nodeName>
```
**Example:** 
```
CREATE (node:Figure {x: 10, y: 15, color: red}) 
RETURN node
```

### Add relationship
Skeleton of the query:
```
MATCH (<nodeName>:<nodeLabel> {<properties>}), (<nodeName>:<nodeLabel> {properties}) 
CREATE (a)-[r:<relationshipName> {properies}]->(b) 
RETURN <nodeName>, <nodeName>

MATCH (<nodeName>:<nodeLabel> {<properties>}), (<nodeName>:<nodeLabel> {properties}) 
CREATE (a)<-[r:<relationshipName> {properies}]-(b) 
RETURN <nodeName>, <nodeName>

MATCH (<nodeName>:<nodeLabel> {<properties>}), (<nodeName>:<nodeLabel> {properties}) 
CREATE (a)-[r:<relationshipName> {properies}]-(b) 
RETURN <nodeName>, <nodeName>
```

**Example:** 
```
MATCH (a:Figure {x: 10}), (b:Figure {x: 10, y:15})
CREATE (a)-[r:LEFT {color: red}]->(b) 
RETURN a, b
```

### Add index
Skeleton of the query:
```
CREATE INDEX (<indexName>:<indexLabel> {<properties>}) 
RETURN <indexName>
```

**Example:**
```
CREATE INDEX (ind:Index {x: 10}) 
RETURN ind
```

### Node removing
Skeleton of the query:
```
REMOVE (<nodeName>:<nodeLabel> {<properties>}) 
RETURN <nodeName>
```

**Example:**
```
REMOVE (node:Figure {x: 10, y:10}) 
RETURN node
```

### Search nodes
#### Get all nodes by label
Skeleton:
```
MATCH (<nodeName>:<nodeLabel>) 
RETURN <nodeName>
```

**Example:**
```
MATCH (node:Figure) 
RETURN node
```

#### Get node by properties
Skeleton:
```
MATCH (<nodeName>:<nodeLabel> {<properties>}) 
RETURN <nodeName>
```

**Example:**
```
MATCH (node:Figure {x: 10, y: 16}) 
RETURN node
```

#### Get nodes by relation
Skeleton:
```
MATCH (<nodeName1>:<nodeLabel1> {<properties>})-[:<relation>]->(<nodeName2>:<nodeLabel2>) 
RETURN <nodeName2>

MATCH (<nodeName1>:<nodeLabel1> {<properties>})-[:<relation> {<properties>}]->(<nodeName2>:<nodeLabel2>) 
RETURN <nodeName2>

MATCH (<nodeName1>:<nodeLabel1> {<properties>})<-[:<relation> {<properties>}]-(<nodeName2>:<nodeLabel2>) 
RETURN <nodeName2>

MATCH (<nodeName1>:<nodeLabel1> {<properties>})-[:<relation> {<properties>}]-(<nodeName2>:<nodeLabel2>) 
RETURN <nodeName2>
```

**Example:**
```
MATCH (node1:Figure {x: 10, y: 19})-[:LEFT]->(node2:Figure) 
RETURN node2

MATCH (node1:Figure {x: 10, y: 19})-[:LEFT {x: 14, color: red}]->(node2:Figure) 
RETURN node2

MATCH (node1:Figure {x: 10, y: 19})<-[:LEFT {x: 14, color: red}]-(node2:Figure) 
RETURN node2

MATCH (node1:Figure {x: 10, y: 19})-[:LEFT {x: 14, color: red}]-(node2:Figure) 
RETURN node2
```

## Running the tests
```
cd lime/tests/

python3 run_tests.py
```

## Built with
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
### Data API

### Graph Engine
- [Rtree 0.8.3](https://pypi.org/project/Rtree/)
- [libspatialindex](http://libspatialindex.github.io/index.html)

### Filesystem

## Screenshots

## Authors
- Gosha Emelyanov - [goshaQ](https://github.com/goshaQ)
- Bulat Maksudov - [Luab](https://github.com/Luab) 
- Kamill Gusmanov - [camilldesmoulins](https://github.com/camilldesmoulins)

## License
This project is licensed under the MIT License.
