import json
from hh_subfun import get_links, get_vacancies
from src.db.requests.DbLoader import DbLoader


def get_hh():
    loader = DbLoader()
    vacancies = []
    for a in get_links():
        vacancies.append(get_vacancies(a))
    with open('data.json', 'a', encoding='utf-8') as f:
        json.dump(vacancies, f, indent=4)
    loader.load(vacancies)

get_hh()
