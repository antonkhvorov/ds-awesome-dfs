import socket
import sys


def listen_for_storage_connection():
    sock = socket.socket()
    sock.bind(('', 9000))
    sock.listen(1000)
    while True:
        conn, address = sock.accept()

        print 'connected:', address
        sys.stdout.flush()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())

        conn.close()


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    print "my ip is", my_ip
    sys.stdout.flush()

    listen_for_storage_connection()