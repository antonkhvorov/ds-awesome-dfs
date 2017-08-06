import shutil
import socket
import sys
import tempfile

from chunks_creator import create_chunks
from utils import recv_message, send_message
from commands import *

client_pwd = "/"


def execute(sock, args):
    if len(args) == 0:
        return

    command = args[0]
    global client_pwd

    if command == "quit":
        send_message(sock, ' '.join(args))
        sock.close()
        exit(0)

    if command == "help":
        help()
        return

    number_of_arguments = {"pwd": [1],
                            "ls": [1, 2],
                            "mkdir": [2],
                            "cd": [2],
                            "cp": [3],
                            "cat": [2],
                            "rm": [2, 3],
                            "stat": [2],
                            "init": [1]
                            }


    if command not in number_of_arguments:
        print "There is no command %s" % command
        help()
        return

    if len(args) not in number_of_arguments[command]:
        print "Wrong number of arguments for %s" % command
        help()
        return

    if command == "ls":  # need for supporting ls [<path>]
        if len(args) == 1:
            args.append(" .")

    if command == "cp":  # generate special message and create chunks for cp command
        # create temp directory
        temp_dir = tempfile.mkdtemp()
        filename = os.path.basename(args[1])  # get name of file
        remote_path = args[2]
        size = os.stat(args[1]).st_size  # get file size
        chunks = create_chunks(os.path.abspath(args[1]), temp_dir)
        args = [command, remote_path, filename, str(size), str(chunks)]

    message = client_pwd + ' ' + ' '.join(args)  # command and arguments

    send_message(sock, message)

    response = recv_message(sock)

    if command == "pwd":
        pwd(response)
    elif command == "ls":
        ls(response)
    elif command == "cd":
        client_pwd = cd(response)
    elif command == "mkdir":
        mkdir(response)
    elif command == "cp":
        cp(response, temp_dir)
        print 'File was copied to the server'
        # remove temp directory
        shutil.rmtree(temp_dir)
    elif command == "rm":
        if len(args) == 2:
            rm_file(response)
        elif len(args) == 3 and args[1] == "-r":
            rm_dir(response)
        else:
            print "Wrong usage of the rm command"
            help()
    elif command == "stat":
        stat(response)
    elif command == "init":
        init(response)


if __name__ == "__main__":

    naming_ip = sys.argv[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))

    while True:
        sys.stdout.write('dfs>>>')
        args = raw_input()
        execute(sock, args.split())
