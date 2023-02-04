import json
import os
import time
from math import ceil

from multiprocessing import Process

from src.db.requests.DbLoader import DbLoader
from src.parsers.hh_parser.HhParser import HhParser

class HhLoader():

    def __init__(self):
        pass

    def get_json_files(self, path):
        files_from_path = os.listdir(path)
        type = ".json"
        json_files = []
        for file in files_from_path:
            if file.endswith(type):
                json_files.append(file)

        return json_files

    def get_core_file_chains(self, path, count_cores):
        json_files = self.get_json_files(path)

        part_len = ceil(len(json_files) / count_cores)
        core_file_chains = [json_files[part_len * k:part_len * (k + 1)] for k in range(count_cores)]

        return core_file_chains

    def load_chain(self, path, json_files):
        dbloader = DbLoader()
        hhparser = HhParser()

        for file_name in json_files:
            json_file_path = path + "\\" + file_name

            with open(json_file_path, encoding='utf-8', mode='r') as f:
                txt_data = f.read()
                txt_data = txt_data.replace('\xa0', '').replace('&quot', '')
            txt_data = '[' + txt_data[:-2] + ']'

            json_data = json.loads(txt_data)

            vacancies = hhparser.get_vacancy_json(json_data)

            dbloader.load(vacancies)

    def load(self, path, count_cores = 3):

        core_file_chains = self.get_core_file_chains(path, count_cores)

        processes = []

        for chain in core_file_chains:
            process = Process(target = self.load_chain, args=(path, chain, ))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()