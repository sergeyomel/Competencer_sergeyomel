import json
from hh_subfun import get_links, get_vacancies
from src.db.requests.DbLoader import DbLoader


def get_hh():
    loader = DbLoader()
    for a in get_links():
        data = json.dumps(get_vacancies(a))

        loader.load(data)