from readUDP import read

class CLI():

    def data_listener(self):
        read()

    def userQueries(self):
        pass


cli = CLI()
cli.data_listener()