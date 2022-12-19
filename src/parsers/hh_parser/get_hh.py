import json
import os

from hh_subfun import get_links, get_vacancies
from src.db.requests.DbLoader import DbLoader


def get_hh():
    loader = DbLoader()
    with open('data.json', 'a', encoding='utf-8') as f:
        f.write('[')
    try:
        for a in get_links():
            data = get_vacancies(a)
            with open('data.json', 'a', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                f.write(',\n')
    except:
        pass
    finally:
        with open('data.json', 'rb+', encoding='utf-8') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()
            f.write(']')
    with open('data.json', 'r', encoding='utf-8') as f:
        data = f.read()
        loader.load(data)


get_hh()
