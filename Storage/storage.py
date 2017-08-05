import socket
import sys

import os
from threading import Thread

from utils import send_message

fake_root = "/fake_root"


def connect_to_naming(naming_ip):
    sock = socket.socket()

    sock.connect((naming_ip, 9000))

    print "connected to", naming_ip
    sys.stdout.flush()


def listen_for_clients_connections():
    sock = socket.socket()
    sock.bind(('', 9001))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()

        print 'Client connected:', address
        sys.stdout.flush()

        t = Thread(target=clients_commands, args=(conn,))
        t.start()

def clients_commands(conn):
    pass

def receive_heartbeat():
    sock = socket.socket()
    sock.bind(('', 9003))
    sock.listen(1)
    while True:
        conn, address = sock.accept()
        print 'Heartbeat from Naming Server received', address
        sys.stdout.flush()
        send_message(conn, "OK")
        conn.close()


def init_fake_root():
    if not os.path.exists(fake_root):
        try:
            os.makedirs(fake_root)
            return ""
        except OSError as e:
            return "Error " + e.message


if __name__ == "__main__":
    init_fake_root()
    my_ip = socket.gethostbyname(socket.gethostname())
    print "my ip is", my_ip
    sys.stdout.flush()

    naming_ip = sys.argv[1]
    connect_to_naming(naming_ip)

    receive_heartbeat()
