import json

from src.db.mocks import mocks
from src.db.requests.DbLoader import DbLoader

if __name__ == "__main__":
    loader = DbLoader()

    path = r'C:\Users\myacc\PycharmProjects\Competencer_sergeyomel\src\db\mocks\indeed.json'
    data = ""
    with open(path, encoding='utf-8', mode='r') as f:
        data = f.read()

    loader.load(data)