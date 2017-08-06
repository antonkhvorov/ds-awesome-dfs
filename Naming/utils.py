import struct
import socket

def send_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)


def recv_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def format_path(path):
    return path if str(path).endswith('/') else str(path) + "/"


def send_file_to_storage(storage_ip, chunk_data):
    sock = socket.socket()
    sock.connect((storage_ip, 9004))
    send_message(sock, chunk_data)
    response = recv_message(sock)
    sock.close()


def get_file_from_storage(storage_ip, filename):
    sock = socket.socket()
    sock.connect((storage_ip, 9004))
    send_message(sock, filename)
    chunk_data = recv_message(sock)
    sock.close()
    return chunk_data