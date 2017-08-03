from ip_pairs import generate_ip_pairs


def pwd(client_pwd):
    return client_pwd


def ls(client_pwd):
    # TODO: implement method
    pass


def cd(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def mkdir(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def touch(client_pwd, args):
    # TODO: implement method
    return ' '.join(args)


def scp(client_pwd, args):
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
