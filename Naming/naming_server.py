import socket
import sys
from time import sleep
from threading import Thread
from commands import *


def listen_for_storage_connection(connected_storages):
    sock = socket.socket()
    sock.bind(('', 9000))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()
        connected_storages.append(address[0])

        print 'Storage connected:', address
        sys.stdout.flush()

        conn.close()


def clients_commands(conn):
    client_pwd = "/"
    while True:
        request = conn.recv(1024)  # 1 KB

        command = request.split()[0]
        args = request.split()[1:]

        if command == "quit":
            conn.close()
            break
        elif command == "pwd":
            response = pwd(client_pwd)
        elif command == "ls":
            response = ls(client_pwd)
        elif command == "cd":
            response = cd(client_pwd, args)
        elif command == "mkdir":
            response = mkdir(client_pwd, args)
        elif command == "touch":
            response = touch(client_pwd, args)
        elif command == "cp":
            response = cp(client_pwd, connected_storages, args)
        elif command == "rm":
            response = rm(client_pwd, args)
        elif command == "stat":
            response = stat(client_pwd, args)

        conn.send(response)


def listen_for_clients_connections():
    sock = socket.socket()
    sock.bind(('', 9001))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()
        connected_storages.append(address[0])

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

            data = sock.recv(1024)  # 1 KB
            if not data:  # if we have not received answer from the Storage Server during heartbeat
                # PERFORM TRANSFER FUNCTION

                pass
            sock.close()
        sleep(60)


# def transfer_to_another_storage():


if __name__ == "__main__":
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
