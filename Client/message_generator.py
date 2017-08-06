import os

from chunks_creator import create_chunks


def generate_message(command, temp_dir, args):
    if command == "cp":
        return generate_cp_message(temp_dir, args)

    pass


# args[0] - filename
def generate_cp_message(temp_dir, args):
    # file name
    name = args[0]
    # get file size
    size = os.stat(name).st_size
    # create chunks and get count of them
    chunks = create_chunks(name, temp_dir)
    return [name, str(size), str(chunks)]
