import shutil
import socket
import sys
import tempfile

from Client.message_generator import generate_message
from commands import *


def execute(args):
    print args

    if len(args) < 3:
        help(args)
        return

    command = args[2]

    if command == "help":
        help(args)
        return

    no_args_commands = ["pwd", "ls"]

    if command not in no_args_commands and len(args) < 3:
        print "Command %s should has arguments"
        help(args)
        return

    commands_with_args = ["cp"]
    if command not in commands_with_args:
        print "There is no command %s"
        help(args)
        return
    # create temp directory
    temp_dir = tempfile.mkdtemp()

    naming_ip = args[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))
    message = command + ' ' + ' '.join(generate_message(command, temp_dir, args[3:]))  # command and arguments
    sock.send(message)

    response = sock.recv(1024)  # 1 KB

    if response != "200":
        print response
        # remove temp directory
        shutil.rmtree(temp_dir)
        return

    if command == "pwd":
        pwd(response)
    elif command == "ls":
        ls(response)
    elif command == "cd":
        cd(response)
    elif command == "mkdir":
        mkdir(response)
    elif command == "touch":
        touch(response)
    elif command == "cp":
        # TODO: Copy file from Naming server using SSH to the temp_dir
        # cp(temp_dir)
        pass
    elif command == "rm":
        rm(response)

    sock.close()
    # remove temp directory
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())
    execute(sys.argv)
