import os

from naming_server import fake_root
from utils import format_path
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
        return "Error incorrect path!"
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


# args[2] - filename
# args[3] - file size
# args[4] - count of chunks
def cp(client_pwd, connected_storages, args):
    if len(args) != 3:
        return "Wrong arguments. Use cp <SOURCE> <DEST>"

    file_name = args[0]
    file_size = args[1]
    chunks = args[2]

    return generate_ip_pairs(file_name, file_size, chunks, connected_storages)


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
