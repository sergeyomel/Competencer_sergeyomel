import json
import os

from src.db.requests.DbLoader import DbLoader
from src.parsers.hh_parser.HhParser import HhParser

class HhLoader():

    def __init__(self):
        self.dbloader = DbLoader()
        self.hhparser = HhParser()

    def load(self, path):

        files_from_path = os.listdir(path)
        type = ".json"
        json_files = []
        for file in files_from_path:
            if file.endswith(type):
                json_files.append(file)

        for file_name in json_files:
            json_file_path = path + "\\" + file_name

            with open(json_file_path, encoding='utf-8', mode='r') as f:
                txt_data = f.read()
                txt_data = txt_data.replace('\xa0', '').replace('&quot', '')

            json_data = json.loads(txt_data)

            vacancies = self.hhparser.get_vacancy_json(json_data)

            self.dbloader.load(json.dumps(vacancies, ensure_ascii=False))

#example
    #hhloader = HhLoader()
    #path = r"C:\Users\myacc\Desktop\jsons"
    #hhloader.load(path)