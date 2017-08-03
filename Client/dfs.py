import socket
from commands import *
import sys


def execute(sock, args):
    command = args[0]

    if command == "quit":
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

    message = ' '.join(args) # command and arguments
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




if __name__ == "__main__":
    my_ip = socket.gethostbyname(socket.gethostname())

    naming_ip = sys.argv[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))

    while True:
        args = raw_input()
        execute(sock, args.split())