import socket
import sys
from time import sleep
from threading import Thread


def listen_for_storage_connection(connected_storages):
    sock = socket.socket()
    sock.bind(('', 9000))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()
        connected_storages.append(address[0])

        print 'Host connected:', address
        sys.stdout.flush()

        conn.close()


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    print "my ip is", my_ip
    sys.stdout.flush()

    connected_storages = list()
    t1 = Thread(target=listen_for_storage_connection, args=(connected_storages,))
    t1.start()


