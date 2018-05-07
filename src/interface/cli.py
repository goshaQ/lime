from readUDP import read
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
                self._interface.get_figures(query)
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


if __name__ == "__main__":    
    cli = CLI()
    cli.userQueryListener()