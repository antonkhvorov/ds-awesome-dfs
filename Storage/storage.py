import socket
import sys

import os
from threading import Thread

from const import fake_root
from utils import send_message, recv_message, format_path

from commands import mkdir


def connect_to_naming(naming_ip):
    sock = socket.socket()

    sock.connect((naming_ip, 9000))

    print "connected to", naming_ip
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


def clients_commands(conn):
    request = recv_message(conn)
    file = request.splitlines()[0]
    chunk_name = os.path.normpath(fake_root + os.path.normpath(file))
    filepath = os.path.dirname(file)
    mkdir(filepath)
    with open(chunk_name, "wb") as out_file:
        for line in request.splitlines()[1:]:
            out_file.write(line)
    print 'Added ', chunk_name
    response = 'OK'
    send_message(conn, response)


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

    receive_heartbeat()


