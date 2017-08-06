import sys
import socket
from threading import Thread
from time import sleep

from commands import *
from utils import recv_message, send_message
from moving import *

fake_root = "/fake_root"


def listen_for_storage_connection(connected_storages):
    sock = socket.socket()
    sock.bind(('', 9000))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()
        if address[0] not in connected_storages:
            connected_storages.add(address[0])

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
            response = cp(client_pwd, list(connected_storages), args)
        elif command == "rm":
            response = rm(client_pwd, args)
        elif command == "stat":
            response = stat(client_pwd, args)
        elif command == "cat":
            response = cat(client_pwd, connected_storages, args)
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


def duplicate_lost_data(lost_storage, connected_storages):
    # TODO: implement actions
    print 'Lost connection with', lost_storage
    sys.stdout.flush()

    files = os.popen('find %s -name "*"' % fake_root).read().split()

    print 'Files:', files
    sys.stdout.flush()

    for filename in files:
        with open(filename, "r") as f:
            for i, line in enumerate(f.splitlines()):
                if i != 0:
                    chunk_ips = line.split('|')
                    second_ip = None
                    if lost_storage == chunk_ips[0]:
                        second_ip = chunk_ips[1]
                    if lost_storage == chunk_ips[1]:
                        second_ip = chunk_ips[0]
                    if second_ip:
                        chunk_name = filename + '/chunk_' + str(i) + '.txt'
                        new_chunk_ip = generate_new_ip(lost_storage, second_ip, connected_storages)
                        move_chunk(chunk_name, second_ip, new_chunk_ip)


def send_heartbeat(connected_storages):
    while True:
        lost = []
        for s in connected_storages:
            try:
                sock = socket.socket()
                sock.connect((s, 9003))
                sock.settimeout(10)
                data = recv_message(sock)
            except:
                duplicate_lost_data(s, connected_storages)
                lost.append(s)
            sock.close()
        for s in lost:
            connected_storages.remove(s)
        sleep(5)


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
    connected_storages = set()
    t1 = Thread(target=listen_for_storage_connection, args=(connected_storages,))
    t1.start()

    t2 = Thread(target=listen_for_clients_connections, args=())
    t2.start()

    heartBeatThread = Thread(target=send_heartbeat, args=(connected_storages,))
    heartBeatThread.start()
