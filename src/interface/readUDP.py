import sys
sys.path.append('')
import socket
from src.interface.interface import Interface
import json

UDP_IP = '127.0.0.1'
UDP_PORT = 9001
INTERFACE = Interface()

def read():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        data = json.loads(data)
        INTERFACE.add_figures(data['data'])
        