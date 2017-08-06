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

    no_args_commands = ["quit", "pwd", "ls"]
    commands_with_args = ["cd", "mkdir", "touch", "scp", "rm", "stat"]

    if command not in no_args_commands + commands_with_args:
        print "There is no command %s" % command
        help()
        return

    if command in commands_with_args and len(args) < 2:
        print "Command %s should has arguments" % command
        help()
        return

    if command == "ls":  # need for supporting ls [<path>]
        if len(args) == 1:
            args.append(" .")

    if command == "scp":  # generate special message and create chunks for cp command
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
    elif command == "touch":
        touch(response)
    elif command == "scp":
        cp(response, temp_dir)
        print 'File was copied to the server'
        # remove temp directory
        shutil.rmtree(temp_dir)
    elif command == "rm":
        rm(response)
    elif command == "stat":
        stat(response)


if __name__ == "__main__":

    naming_ip = sys.argv[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))

    while True:
        args = raw_input()
        execute(sock, args.split())
