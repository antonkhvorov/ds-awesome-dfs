import shutil
import sys
import tempfile

from chunks_creator import create_chunks
from commands import *
from logger import get_logger

client_pwd = "/"
logger = get_logger('client_dfs')


def execute(sock, args):
    if len(args) == 0:
        logger.warn('No args were entered!')
        return

    command = args[0]
    global client_pwd

    if command == "quit":
        send_message(sock, ' '.join(args))
        sock.close()
        logger.info('Client pwd: %s ; Process finished with exit code 0' % client_pwd)
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
        logger.info('Client pwd: %s ; There is no command %s' % (client_pwd, command))
        help()
        return

    if len(args) not in number_of_arguments[command]:
        print "Wrong number of arguments for %s" % command
        logger.info('Wrong number of arguments for %s' % command)
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
        logger.info('Client pwd: %s ; %s chunks were created' % (client_pwd, str(chunks)))
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
        # remove temp directory
        shutil.rmtree(temp_dir)
    elif command == "rm":
        rm(response)
    elif command == "stat":
        stat(response)
    elif command == "init":
        init(response)
    elif command == "cat":
        cat(response)


if __name__ == "__main__":

    naming_ip = sys.argv[1]
    sock = socket.socket()
    sock.connect((naming_ip, 9001))
    logger.info('Connected to the Naming server: %s' % naming_ip)

    while True:
        sys.stdout.write('dfs>>>')
        args = raw_input()
        logger.info('Client pwd: %s ; Input string: %s' % (client_pwd, args))
        execute(sock, args.split())
