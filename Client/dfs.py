import socket
from time import sleep
import sys


def pwd(response):
    # TODO: implement method
    pass


def ls(response):
    # TODO: implement method
    pass


def cd():
    # TODO: implement method
    pass


def mkdir():
    # TODO: implement method
    pass


def touch():
    # TODO: implement method
    pass


def cp(response):
    # TODO: implement method
    pass


def rm(response):
    # TODO: implement method
    pass


def help(args):
    print "Use $s <namig server ip> <command> [<arguments>]" % args[0]
    # TODO: describe all commands


def execute(args):
    if len(args) < 3:
        help(args)
        return

    command = args[2]

    if command == "help":
        help(args)
        return

    no_args_commands = ["pwd", "ls"]

    if command not in no_args_commands:
        print "Command %s should has arguments"
        help(args)
        return

    commands_with_args = []
    if command not in no_args_commands or command not in commands_with_args:
        print "There is no command %s"
        help(args)
        return

    naming_ip = args[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))
    message = ' '.join(args[2:]) # command and arguments
    sock.send(message)

    if command == "pwd":
        response = sock.recv(1024)  # 1 KB
        pwd(response)
    elif command == "ls":
        response = sock.recv(1024)  # 1 KB
        ls(response)
    elif command == "cd":
        cd()
    elif command == "mkdir":
        mkdir()
    elif command == "touch":
        touch()
    elif command == "cp":
        response = sock.recv(1048576)  # 1 MB
        cp(response)
    elif command == "rm":
        response = sock.recv(1048576)  # 1 MB
        rm(response)

    sock.close()


if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())

    execute(sys.argv)