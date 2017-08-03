from Naming.ip_pairs import generate_ip_pairs


def pwd():
    # TODO: implement method
    pass


def ls():
    # TODO: implement method
    pass


def cd(args):
    # TODO: implement method
    pass


def mkdir(args):
    # TODO: implement method
    pass


def touch(args):
    # TODO: implement method
    pass


# args[0] - filename
# args[1] - file size
# args[2] - count of chunks
def cp(connected_storages, args):
    if len(args) != 3:
        # TODO Handle exception
        return "400"
    generate_ip_pairs(args[0], args[1], args[2], connected_storages)
    # TODO change return status
    return "200"

def rm(args):
    # TODO: implement method
    pass