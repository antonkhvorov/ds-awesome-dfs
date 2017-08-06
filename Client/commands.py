import os
import socket


from logger import get_logger
from utils import send_message, recv_message, format_path

logger = get_logger('client_commands')

def pwd(response):
    logger.info('Command pwd response: %s' % response)
    print response


def ls(response):
    logger.info('Command ls response: %s' % response)
    print response


def cd(response):
    logger.info('Command cd response: %s' % response)
    return response


def mkdir(response):
    logger.info('Command mkdir response: %s' % response)
    print response


def cp(response, temp_dir):
    original_file = response
    for i, line in enumerate(original_file.splitlines()):
        if i == 0:
            filepath = line.split('|')[0]
        else:
            #  send file to storage
            # format came from chunks_creator
            chunk_name = format_path(temp_dir) + os.path.basename(filepath) + '/chunk_' + str(i) + '.txt'
            chunk_data = format_path(filepath) + 'chunk_' + str(i) + '.txt' + os.linesep
            with open(chunk_name, 'r') as chunk:
                chunk_data += chunk.read() + os.linesep
            print chunk_name
            print chunk_data
            send_file_to_storage(line.split('|')[0], chunk_data)
            # send copy of file to storage
            if (line.split('|')[1] != ''):
                send_file_to_storage(line.split('|')[1], chunk_data)


def stat(response):
    # TODO: implement method
    logger.info('Command stat response: %s' % response)
    print response


def rm(response):
    # TODO: implement method
    logger.info('Command rm response: %s' % response)
    print response


def init(response):
    # TODO: implement method
    logger.info('Command init response: %s' % response)
    print response

def cat(response):
    for line in response.splitlines():
        print(line)
    logger.info('Command cat response was printed')




def help():
    print "Available commands:"
    print "quit"
    print "help"
    print "pwd"
    print "ls [directory]"
    print "mkdir <directory>"
    print "cd <directory>"
    print "cp <file> <location>"
    print "cat <file>"
    print "rm <file or directory> "
    print "stat <file or directory>"
    print "init"
    logger.info('Command help response: comands were printed')


def send_file_to_storage(storage_ip, chunk_data):
    sock = socket.socket()
    sock.connect((storage_ip, 9004))
    send_message(sock, chunk_data)
    logger.info('Command cp response: Sent %s to the storage %s' % (os.path.basename(chunk_data.splitlines()[0]), storage_ip))
    response = recv_message(sock)
    logger.info(
        'Command cp response: Storage %s response: %s' % (storage_ip, response))
    sock.close()

