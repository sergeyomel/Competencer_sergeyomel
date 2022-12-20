import json
import os

from hh_subfun import get_links, get_vacancies
from src.db.requests.DbLoader import DbLoader


def get_hh():
    loader = DbLoader()
    vacancies = []
    for a in get_links():
        data = get_vacancies(a)
        vacancies.append(data)
        loader.load(vacancies)
        vacancies.pop()

get_hh()
