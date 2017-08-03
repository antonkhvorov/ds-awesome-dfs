import os
import re


def create_chunks(file_object, temp_dir, chunk_size=1024):
    # Cause a single word can not be split into different chunks, count of bytes
    # could be changed according to the last word in previous chunk
    work_chunk_size = chunk_size
    with open(file_object, "rb") as in_file:
        # counter for out files
        num = 1
        # last word from previous chunk (if it was split)
        last_word = b''
        while True:
            chunk = last_word + in_file.read(work_chunk_size)
            if not chunk:
                break  # end of file
            # the next byte shows, is the last word in chunk full or not
            ch = in_file.read(1)
            if ch in [b' ', b'\n', b'\r', b'\t', b'']:
                last_word = ch
                work_chunk_size = chunk_size - 1
            else:
                last_word = bytes(re.split(' |\r\n|\n|\t', unicode(chunk))[-1])
                if last_word != chunk:
                    chunk = chunk[0:len(chunk) - len(last_word)]
                    last_word += ch  # add next byte
                    work_chunk_size = chunk_size - len(last_word) - 1
                else:
                    last_word = ch
                    work_chunk_size = chunk_size
            # create chunk in the temp directory with the path as original file
            chunk_name = temp_dir + os.path.abspath(file_object) + '/chunk ' + str(num) + '_' + os.path.basename(
                file_object)
            if not os.path.exists(os.path.dirname(chunk_name)):
                os.makedirs(os.path.dirname(chunk_name))
            with open(chunk_name, "wb") as out_file:
                out_file.write(chunk)
                num = num + 1
    return num - 1
