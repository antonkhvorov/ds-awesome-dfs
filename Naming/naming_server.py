import sys
import socket
from threading import Thread
from time import sleep

from commands import *
from utils import recv_message, send_message

fake_root = "/fake_root"


def listen_for_storage_connection(connected_storages):
    sock = socket.socket()
    sock.bind(('', 9000))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()
        if address[0] not in connected_storages:
            connected_storages.append(address[0])

        print 'Storage connected:', address
        sys.stdout.flush()

        conn.close()


def clients_commands(conn):
    while True:
        request = recv_message(conn)
        print request
        sys.stdout.flush()
        req = request.split()
        client_pwd = req[0]
        command = req[1]
        args = req[2:]
        response = "nothing"

        if command == "quit":
            conn.close()
            break
        elif command == "pwd":
            response = pwd(client_pwd)
        elif command == "ls":
            response = ls(client_pwd, args)
        elif command == "cd":
            response = cd(client_pwd, args)
        elif command == "mkdir":
            response = mkdir(client_pwd, args)
        elif command == "cp":
            response = cp(client_pwd, connected_storages, args)
        elif command == "rm":
            response = rm(client_pwd, args)
        elif command == "stat":
            response = stat(client_pwd, args)
        elif command == "init":
            response = init(client_pwd, args)

        send_message(conn, response)


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


def send_heartbeat(connected_storages):
    while True:
        for s in connected_storages:
            sock = socket.socket()
            sock.connect((s, 9003))
            sock.settimeout(10)

            data = recv_message(sock)
            if not data:  # if we have not received answer from the Storage Server during heartbeat
                # PERFORM TRANSFER FUNCTION

                pass
            sock.close()
        sleep(60)


# def transfer_to_another_storage():

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
    connected_storages = list()
    t1 = Thread(target=listen_for_storage_connection, args=(connected_storages,))
    t1.start()

    t2 = Thread(target=listen_for_clients_connections, args=())
    t2.start()

    heartBeatThread = Thread(target=send_heartbeat, args=(connected_storages,))
    heartBeatThread.start()
