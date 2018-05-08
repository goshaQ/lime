import sys
sys.path.append('')
from src.interface.readUDP import read
from src.interface.interface import Interface
import threading

CLI_FILE = 'src/interface/cli_start.txt'

class CLI():
    def __init__(self):
        self._interface = Interface()
        thread = threading.Thread(target=self.dataListener, args=())
        thread.daemon = True
        thread.start()

    def dataListener(self):
        read()

    def userQueryListener(self):
        f = open(CLI_FILE, 'r')
        print(f.read())
        # TODO; add showing results
        while True:
            user_input = input(">>> ")
            if ":help" in user_input:
                print("RTFM -> https://github.com/goshaQ/lime")
            elif ":search" in user_input:
                query = input("Enter query: ")
                result = self._interface.get_figures(query)
                for key, value in result.items():
                    self._toString(value)
            elif ":node" in user_input:
                query = input("Enter query: ")
                self._interface.add_figure(query)
            elif ":relationship" in user_input:
                query = input("Enter query: ")
                self._interface.add_relationship(query)
            elif ":index" in user_input:
                query = input("Enter query: ")
                self._interface.add_index(query)
            elif ":remove" in user_input:
                query = input("Enter query: ")
                self._interface.remove_node(query)
            elif ":quit" in user_input:
                print("Bye!")
                break
            else:
                print("RTFM. Type ':help'")

    def _toString(self, value):
        for v in value:
            template = "Label: %s;" %(v.label.value)
            next_prop = v.next_prop
            properties = []
            while next_prop is not None:
                properties.append(next_prop.value)
                next_prop = next_prop.next_prop
            i = 1
            for p in properties:
                template += " property_%s: %s;" %(str(i), str(p))
                i += 1
            print(template)

if __name__ == "__main__":    
    cli = CLI()
    cli.userQueryListener()


# MATCH (node1:Figure {x: 10, y: 15})-[:LEFT]->(node2:Figure) RETURN node2

# CREATE (node:Figure {x: 5, y: 15, color: red}) RETURN node

# MATCH (a:Figure {x: 10, y:15}), (b:Figure {x: 5, y:15}) CREATE (a)-[r:LEFT {color: red}]->(b) RETURN a, b