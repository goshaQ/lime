from readUDP import read
from src.interface.interface import Interface

CLI_FILE = 'src/interface/cli_start.txt'

class CLI():
    def __init__(self):
        self._interface = Interface()

    def data_listener(self):
        read()

    def userQueries(self):
        f = open(CLI_FILE, 'r')
        print(f.read())
        while True:
            user_input = input(">>> ")
            if ":help" in user_input:
                print("RTFM -> https://github.com/goshaQ/lime")
            elif ":search" in user_input:
                query = input("Enter query: ")
                self._interface.get_figures(query)
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


cli = CLI()
# cli.data_listener()
cli.userQueries()