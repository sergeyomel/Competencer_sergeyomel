import os.path
import os
import subprocess
#from scr.db.requests.DbLoader import DbLoader
import json


def upload_from_indeed(file_path):
    #uploader = DbLoader()
    with open(file_path, 'r') as indeed_json:
        data = json.dumps(indeed_json)
    for vacancy in data:
        id = vacancy['parsing']['id']
        ids_from_db = "" #запрос к бд
        if id not in ids_from_db:
            #uploader.load(vacancy)
            pass

if __name__ == "__main__":
    path = r"."
    subprocess.call([f"cd {path}", r"venv\Scripts\activate", "cd indeed-parser-project", f"scrapy crawl indeed_jobs"])



