import os

from utils import format_path
from const import fake_root


def touch(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def cp(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def rm(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def mkdir(path):
    path = os.path.normpath(path)
    real_path = os.path.normpath(fake_root + path)

    if not os.path.exists(real_path):
        try:
            os.makedirs(real_path)
            return ""
        except:
            return "Unable to create directory!"
    else:
        return "Directory " + format_path(path) + " already exists!"
