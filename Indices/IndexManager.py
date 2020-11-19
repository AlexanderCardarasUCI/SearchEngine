from Tokenizer import IndexBuilder
from Utils import Constants
import os
import json
import ast
from Utils import Timer


class Backend:
    def __init__(self):
        self.id_url = {}
        self.inverted_index = {}
        self.token_locations = {}
        self.download_indices()

    def download_indices(self):
        if self.indices_are_built():
            print("[Log] Loading Indices To Main Memory")

            self.id_url = IndexBuilder.parse_index(Constants.ID_URL_PATH)
            self.token_locations = IndexBuilder.parse_index(Constants.TOKEN_LOCATION_PATH)
        else:
            print("[Log] Creating Indices And Loading Them To Main Memory")
            IndexBuilder.build_inverted_index(Constants.DEV_PATH)

            self.id_url = IndexBuilder.parse_index(Constants.ID_URL_PATH)
            self.token_locations = IndexBuilder.parse_index(Constants.TOKEN_LOCATION_PATH)

    def get_id_url(self):
        return self.id_url

    def indices_are_built(self):
        required_files = [Constants.ID_URL_PATH, Constants.INVERTED_INDEX_PATH, Constants.TOKEN_LOCATION_PATH]
        for rf in required_files:
            if len(os.listdir(rf)) == 0:
                return False

        return True

    def get_number_of_docs(self):
        return len(self.id_url)

    def get_docs_with_term(self, term):
        if term in self.token_locations:
            doc_num, position = self.token_locations[term]
            data = self.parse_inverted_index(Constants.INVERTED_INDEX_NAME+str(doc_num)+".json", position)
            return data[term]
        else:
            return []

    def parse_inverted_index(self, doc, start):
        data = {}
        with open(Constants.INVERTED_INDEX_PATH+doc) as file:
            file.seek(start)
            line = file.readline()

            key, value = line.split(Constants.SPLIT)
            line = "{\""+key+"\":"+value+"}"
            data[str(key)] = json.loads(line)[key]

        return data
