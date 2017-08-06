import os

from utils import format_path
from const import fake_root


def cp(args):
    file = args.splitlines()[0]
    chunk_name = os.path.normpath(fake_root + os.path.normpath(file))
    filepath = os.path.dirname(file)
    mkdir(filepath)
    with open(chunk_name, "wb") as out_file:
        for line in args.splitlines()[1:]:
            out_file.write(line + os.linesep)
    print 'Added ', chunk_name
    response = 'OK'
    return response


def cat(args):
    filepath = args
    chunk_name = os.path.normpath(fake_root + filepath)
    chunk_data = ''
    try:
        with open(chunk_name, 'r') as chunk:
            chunk_data += chunk.read()
    except:
        return "400"
    return chunk_data


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
