
from Tokenizer import FileParser
from Tokenizer import Tokenize
from Utils import Constants
import time
import os
import ast

def parse_index(index_path, index_name=None, start=None):
    data = {}

    if index_name is not None:
        full_path = index_path + index_name
    else:
        files = os.listdir(index_path)
        full_path = index_path + files[0]

    with open(full_path) as file:

        if start is not None:
            file.seek(start)
            line = file.readline()
            key, value = line.split(Constants.SPLIT)
            try:
                data[str(key)] = ast.literal_eval(value)
            except:
                data[str(key)] = str(value)

            return data
        else:
            while True:
                line = file.readline()
                if len(line) == 0:
                    break
                key, value = line.split(Constants.SPLIT)
                try:
                    data[str(key)] = ast.literal_eval(value)
                except:
                    data[str(key)] = str(value)

        return data


def merge_write(path):

    while len(os.listdir(path)) > 1:
        files = os.listdir(path)
        i = 1
        while i < len(files):
            l1 = parse_index(Constants.INVERTED_INDEX_PATH, index_name=files[i - 1])
            l2 = parse_index(Constants.INVERTED_INDEX_PATH, index_name=files[i])

            for token in l2:
                if token in l1:
                    for t in l2[token]:
                        l1[token].append(t)
                else:
                    l1[token] = l2[token]

            os.remove(path+files[i-1])
            os.remove(path+files[i])
            sort_and_write_to_disk(l1, path+files[i-1])
            # write_dictionary_to_file(l1, path+files[i-1])
            i+=2


def write_dictionary_to_file(dictionary, filename):
    with open(filename, 'w') as fp:
        for key in dictionary:
            fp.write(str(key)+Constants.SPLIT+str(dictionary[key])+"\n")


def sort_dictionary(dictionary, key=None):
    sort_dic = {}
    Y = sorted(dictionary,key=key)
    for token in Y:
        sort_dic[token] = dictionary[token]

    return sort_dic


def sort_and_write_to_disk(I, name):
    sorted_dict = sort_dictionary(I)
    write_dictionary_to_file(sorted_dict, name)


def build_inverted_index(base_path):
    name = 0
    I = {}
    id_to_url = {}

    paths = FileParser.get_file_names(base_path)
    # paths = paths[0:1000]
    batch_point = 0
    n = 0

    start_time = time.time()

    while batch_point != -1:
        B, batch_point = get_batch(paths, batch_point, 5000)
        # B, batch_point = get_batch(paths, batch_point, 100)
        for d in B:
            n += 1
            url, content = FileParser.get_url_content(d)
            text = FileParser.html_to_text(content)

            T = Tokenize.tokenize(text)
            frequencies, positions = Tokenize.compute_token_analytics(T)
            T = Tokenize.remove_duplicates(T)
            id_to_url[n] = url

            for t in T:
                if t not in I:
                    I[t] = [[n, frequencies[t]]]
                else:
                    I[t].append([n, frequencies[t]])

        name += 1
        sort_and_write_to_disk(I, Constants.INVERTED_INDEX_PATH+Constants.INVERTED_INDEX_NAME+(name.__str__())+".json")
        I = {}

        end_time = time.time()
        print(batch_point, (end_time - start_time))
        start_time = time.time()

    merge_write(Constants.INVERTED_INDEX_PATH)
    sort_and_write_to_disk(id_to_url, Constants.ID_URL_PATH+Constants.ID_URL_NAME+".json")
    split_inverted_index(10, len(id_to_url))


def split_inverted_index(num_parts, total_lines):

    token_location = {}
    data = {}
    lines_read = 0
    file_number = 1000
    last_pos = 0
    files = os.listdir(Constants.INVERTED_INDEX_PATH)
    with open(Constants.INVERTED_INDEX_PATH + files[0]) as file:
        while True:
            if lines_read > (total_lines/num_parts)+1:

                write_dictionary_to_file(data,
                                         Constants.INVERTED_INDEX_PATH + Constants.INVERTED_INDEX_NAME + str(file_number) + ".json")
                file_number += 1
                lines_read = 0
                data = {}
                last_pos = file.tell()

            pos = file.tell()
            line = file.readline()

            if len(line) == 0:
                break

            key, value = line.split(Constants.SPLIT)
            try:
                data[str(key)] = ast.literal_eval(value)
            except:
                data[str(key)] = str(value)

            token_location[str(key)] = [file_number, pos-last_pos]
            lines_read += 1

    write_dictionary_to_file(token_location, Constants.TOKEN_LOCATION_PATH + Constants.TOKEN_LOCATION_NAME + ".json")
    write_dictionary_to_file(token_location,
                             Constants.INVERTED_INDEX_PATH + Constants.INVERTED_INDEX_NAME + str(file_number) + ".json")
    return token_location


def build_token_location():
    data = {}
    total_bytes = 0
    files = os.listdir(Constants.INVERTED_INDEX_PATH)
    with open(Constants.INVERTED_INDEX_PATH+files[0]) as file:
        while True:
            pos = file.tell()
            line = file.readline()
            if len(line) == 0:
                break
            key, value = line.split(Constants.SPLIT)
            data[str(key)] = pos
            total_bytes += len(line)

    write_dictionary_to_file(data, Constants.TOKEN_LOCATION_PATH+Constants.TOKEN_LOCATION_NAME+".json")
    return data


def get_batch(paths, starting_point, batch_size):
    end_point = starting_point+batch_size
    if end_point > len(paths):
        return paths[starting_point:], -1
    else:
        return paths[starting_point:end_point], end_point
