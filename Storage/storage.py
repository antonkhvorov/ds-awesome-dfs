import socket
from time import sleep
import sys


def connect_to_naming(naming_ip):
    sock = socket.socket()

    sock.connect((naming_ip, 9000))

    print "connected to", naming_ip
    sys.stdout.flush()

    sleep(30)


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    print "my ip is", my_ip
    sys.stdout.flush()

    naming_ip = sys.argv[1]
    connect_to_naming(naming_ip)