import os
import socket

from naming_server import fake_root
from utils import format_path, send_message, recv_message
from ip_pairs import generate_ip_pairs


def pwd(client_pwd):
    return client_pwd


def ls(client_pwd, args):
    if len(args) != 1:
        return "Error not enough arguments! Use: ls [<arguments>]"

    path = os.path.normpath(format_path(client_pwd) + args[0])
    real_path = os.path.normpath(fake_root + path)
    try:
        listdir = os.listdir(real_path)
    except Exception as e:
        return "Error incorrect path!!"
    return os.linesep.join(str(name) for name in listdir)


def cd(client_pwd, args):
    if len(args) != 1:
        return "Error not enough arguments! Use: cd <argument>"

    path = os.path.normpath(format_path(client_pwd) + args[0])
    real_path = os.path.normpath(fake_root + path)

    if os.path.exists(real_path):
        os.chdir(real_path)
        return path
    else:
        return client_pwd


def mkdir(client_pwd, args):
    if len(args) != 1:
        return "Error not enough arguments! Use: mkdir <argument>"

    path = os.path.normpath(format_path(client_pwd) + args[0])
    real_path = os.path.normpath(fake_root + path)

    if not os.path.exists(real_path):
        try:
            os.makedirs(real_path)
            return ""
        except:
            return "Unable to create directory!"
    else:
        return "Directory " + format_path(args[0]) + " already exists!"


def touch(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


# args[0] - remote_path
# args[1] - filename
# args[2] - file size
# args[3] - count of chunks
def cp(client_pwd, connected_storages, args):
    if len(args) != 4:
        return "Wrong arguments. Use cp <SOURCE> <DEST>"
    remote_path = args[0]
    file_name = args[1]
    file_size = args[2]
    chunks = args[3]

    if remote_path == '.':
        remote_address = format_path(client_pwd) + file_name
    else:
        remote_address = (format_path(remote_path) if remote_path.startswith('/') else "/" + format_path(remote_path)) \
                         + file_name

    return generate_ip_pairs(remote_address, file_size, chunks, connected_storages)


def rm(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def stat(client_pwd, args):
    if len(args) != 1:
        return "Error not enough arguments! Use: stat <argument>"

    path = os.path.normpath(format_path(client_pwd) + args[0])
    real_path = os.path.normpath(fake_root + path)

    if not os.path.exists(real_path):
        return "Error path " + path + "not exists!"
    else:
        if os.path.isdir(real_path):
            try:
                listdir = os.listdir(real_path)
                return "Directory " + path + " contains " + str(len(listdir)) + " items"
            except Exception as e:
                return "Unable to get directory stats!"

        if os.path.isfile(real_path):
            try:
                with open(real_path) as f:
                    file_data = f.readline().split("|")
                    f.close()
                    return "File size: " + file_data[1] + os.linesep + "Divided on: " + file_data[2] + " chunks"
            except:
                return "Unable to get file stats!"


def cat(client_pwd, connected_storages, args):
    if len(args) != 1:
        return "Error not enough arguments! Use: stat <argument>"
    # file in the pwd directory
    filepath = os.path.normpath(format_path(client_pwd) + args[0])
    real_path = os.path.normpath(fake_root + filepath)
    if not os.path.exists(real_path):
        return "Error path %s not exists!" % filepath
    else:
        with open(real_path, 'r') as read_file:
            full_file = ''
            lcount = 0
            for i, line in enumerate(read_file):
                print '%s %s' %(i, line)
                if i == 0:
                    remote_path = line.split('|')[0]
                    chunks = line.split('|')[2]
                    print "chunks = ", chunks
                if i > 0:
                    chunk_path = format_path(remote_path) + 'chunk_' + str(i) + '.txt'
                    if ip_in_list(line.split('|')[0], connected_storages):
                        full_file += request_chunk_from_storage(line.split('|')[0], chunk_path)
                    elif ip_in_list(line.split('|')[1], connected_storages):
                        full_file += request_chunk_from_storage(line.split('|')[1], chunk_path)
                    else:
                        return "Some chunk of %s file is not exist" % filepath
                    lcount += 1
                    print lcount

        if lcount != int(chunks):
            return "Some chunk of %s file is not exist" % filepath
        else:
            return full_file



def ip_in_list(ip, connected_storages):
    return True if ip in connected_storages else False


def request_chunk_from_storage(storage_ip, chunk_path):
    sock = socket.socket()
    sock.connect((storage_ip, 9005))
    send_message(sock, chunk_path)
    response = recv_message(sock)
    sock.close()
    return response
