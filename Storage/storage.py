import socket
import sys

import os
from threading import Thread

from const import fake_root
from utils import send_message, recv_message

from commands import mkdir, cp, cat


def connect_to_naming(naming_ip):
    sock = socket.socket()

    sock.connect((naming_ip, 9000))

    print "Connected to", naming_ip
    sys.stdout.flush()


def listen_for_clients_connections():
    sock = socket.socket()
    sock.bind(('', 9004))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()

        print 'Client connected:', address
        sys.stdout.flush()

        t = Thread(target=clients_commands, args=(conn,))
        t.start()


def listen_for_naming_connections():
    sock = socket.socket()
    sock.bind(('', 9005))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()

        print 'Naming connected:', address
        sys.stdout.flush()

        t = Thread(target=naming_commands, args=(conn,))
        t.start()


def clients_commands(conn):
    request = recv_message(conn)
    if len(request) < 2:
        return
    command = request[0]

    if command == "cp":
        send_message(conn, cp(request[1]))

    elif command == "cat":
        send_message(conn, cat(request[1]))


def naming_commands(conn):
    request = recv_message(conn)
    filepath = request
    chunk_name = os.path.normpath(fake_root + filepath)
    chunk_data = ''
    with open(chunk_name, 'r') as chunk:
        chunk_data += chunk.read()
    send_message(conn, chunk_data)


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

    t2 = Thread(target=listen_for_clients_connections, args=())
    t2.start()

    t3 = Thread(target=listen_for_naming_connections, args=())
    t3.start()

    receive_heartbeat()
