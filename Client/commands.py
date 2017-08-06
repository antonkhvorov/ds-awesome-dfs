import os
import socket

from utils import send_message, recv_message, format_path


def pwd(response):
    print response


def ls(response):
    print response


def cd(response):
    return response


def mkdir(response):
    print response


def touch(response):
    # TODO: implement method
    print response


def cp(response, temp_dir):
    original_file = response
    for i, line in enumerate(original_file.splitlines()):
        if i == 0:
            filepath = line.split('|')[0]
        else:
            #  send file to storage
            # format came from chunks_creator
            chunk_name = format_path(temp_dir) + os.path.basename(filepath) + '/chunk_' + str(i) + '.txt'
            chunk_data = format_path(filepath) + 'chunk_' + str(i) + '.txt' + os.linesep
            with open(chunk_name, 'r') as chunk:
                chunk_data += chunk.read()
            send_file_to_storage(line.split('|')[0], chunk_data)
            # send copy of file to storage
            if (line.split('|')[1] != ''):
                send_file_to_storage(line.split('|')[1], chunk_data)


def stat(response):
    # TODO: implement method
    print response


def rm(response):
    # TODO: implement method
    print response


def help():
    print "Use <command> [<arguments>]"
    # TODO: describe all commands


def send_file_to_storage(storage_ip, chunk_data):
    sock = socket.socket()
    sock.connect((storage_ip, 9004))
    send_message(sock, chunk_data)
    request = recv_message(sock)
    sock.close()

