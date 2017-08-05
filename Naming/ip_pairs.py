import os
import random


def generate_ip_pairs(file_name, file_size, chunks, ips):
    output_str = os.path.abspath(file_name) + "|" + file_size + "|" + chunks + os.linesep

    i = 0
    while i < int(chunks):
        output_str += get_ip_pair(ips) if (i == int(chunks) - 1) else get_ip_pair(ips) + os.linesep
        i += 1

    text_file = open(file_name, "w")
    text_file.write(output_str)
    text_file.close()
    return output_str


def get_ip_pair(ips):
    if len(ips) == 1:
        return str(ips[0]) + "|"
    else:
        i = -1
        j = -1
        while True:
            i = random.randint(0, len(ips) - 1)
            j = random.randint(0, len(ips) - 1)
            if i != j and i != -1 and j != -1:
                break

        return str(ips[i]) + "|" + str(ips[j])
