import random
from utils import *

def generate_new_ip(lost_ip, second_ip, ips):
    available_ips = list(set(ips) - {lost_ip, second_ip})

    if len(available_ips) == 0:
        return second_ip
    else:
        i = random.randint(0, len(available_ips) - 1)
        return available_ips[i]


def move_chunk(chunk_name, second_ip, new_chunk_ip):
    chunk_data = get_file_from_storage(new_chunk_ip, chunk_name)
    send_file_to_storage(new_chunk_ip, chunk_data)