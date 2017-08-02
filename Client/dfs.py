import socket
from time import sleep
import sys


def connect_to_naming(naming_ip):
    sock = socket.socket()

    sock.connect((naming_ip, 9001))

    print "connected to", naming_ip
    sys.stdout.flush()

    print "Text to send:",
    text = raw_input()
    sock.send(text)

    data = sock.recv(1024)  # 1 KB
    sock.close()

    print data
    sys.stdout.flush()


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())

    naming_ip = sys.argv[1]
    connect_to_naming(naming_ip)