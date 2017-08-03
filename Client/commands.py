import os


def pwd(response):
    print response

def ls(response):
    # TODO: implement method

    print response

def cd(response):
    # TODO: implement method
    print response


def mkdir(response):
    # TODO: implement method
    print response


def touch(response):
    # TODO: implement method
    print response


def cp(temp_dir):
    # TODO: Copy file from Naming server using SSH to the temp_dir
    original_file = "../data/1_ips.txt" #set the name of file with ips
    with open(original_file, "rb") as in_file:
        for i, line in enumerate(in_file):
            if i == 0:
                filepath = line.split('|')[0]
            else:
                #  send file to storage
                # format came from chunks_creator
                chunk_name = temp_dir + filepath + '/chunk ' + str(i) + '_' + os.path.basename(filepath)
                send_file_to_storage(line.split('|')[0], chunk_name)
                # send copy of file to storage
                if(line.split('|')[1] != os.linesep):
                    send_file_to_storage(line.split('|')[1], chunk_name)

def stat(response):
    # TODO: implement method
    print response


def rm(response):
    # TODO: implement method
    print response


def help():
    print "Use <command> [<arguments>]"
    # TODO: describe all commands


def send_file_to_storage(storage_ip, chunk):
    # TODO: implement method
    print storage_ip
    with open(chunk, "rb") as in_file:
        for line in in_file:
            print line
    pass
