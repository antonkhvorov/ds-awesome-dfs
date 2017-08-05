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


# args[0] - filename
# args[1] - file size
# args[2] - count of chunks
def cp(client_pwd, connected_storages, args):
    if len(args) != 3:
        # TODO Handle exception
        return "400"
    generate_ip_pairs(args[0], args[1], args[2], connected_storages)
    # TODO change return status
    return "200"


def rm(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def stat(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)
