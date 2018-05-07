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
- Reading the data from UDP (ip='127.0.0.1', port=9001)
- Reading user queries

### User queries
- :help - if you want to read helper
- :node - if you want to add a new node
- :search - if you want to search in the Database
- :relationship - if you want to add a new relationship
- :index - if you want to add an index
- :remove - if you want to remove the node
- :quit - close the program

### Insert nodes
There are two possible ways for adding data to the database:
- Through UDP messages (mentioned before)
- Using SimpleCypherQL queries

If you want to add the node, type bu this skeleton:
```
CREATE (<nodeName>:<nodeLabel> {<properties>}) RETURN node
```
**Example** - `CREATE (node:Figure {x: 10, y: 15, color: red}) RETURN node`

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
