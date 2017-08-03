import itertools
import os


def generate_ip_pairs(file_name, file_size, chunks, ips):

    output_str = os.path.abspath(file_name) + "|" + file_size + "|" + chunks + "\n"

    for pair in itertools.combinations(ips, 2):
        pair = str(pair).replace("(", "").replace(")", "\n").replace(", ", "|").replace("\'", "").replace("\"", "")
        print pair
        output_str += pair

    print output_str
    text_file = open(file_name, "w")
    text_file.write(output_str)
    text_file.close()

