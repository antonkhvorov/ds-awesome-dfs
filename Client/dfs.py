import socket
from time import sleep
from commands import *
import sys


def execute(args):
    if len(args) < 3:
        help(args)
        return

    command = args[2]

    if command == "help":
        help(args)
        return

    no_args_commands = ["pwd", "ls"]

    commands_with_args = ["cd", "mkdir", "touch", "scp", "rm", "stat"]
    if command not in no_args_commands and command not in commands_with_args:
        print "There is no command %s" % command
        help(args)
        return

    if command not in no_args_commands and len(args) < 4:
        print "Command %s should has arguments" % command
        help(args)
        return

    naming_ip = args[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))
    message = ' '.join(args[2:]) # command and arguments
    sock.send(message)

    response = sock.recv(1024)  # 1 KB

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
    elif command == "scp":
        scp(response)
    elif command == "rm":
        rm(response)
    elif command == "stat":
        stat(response)

    sock.close()


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())

    execute(sys.argv)