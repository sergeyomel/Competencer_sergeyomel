import json
import os

from hh_subfun import get_links, get_vacancies
from src.db.requests.DbLoader import DbLoader


def get_hh():
    count_json_items = 10

    loader = DbLoader()
    vacancies = []
    curr_link_num = 0

    for link in get_links():
        vacancy = get_vacancies(link)
        vacancies.append(vacancy)

        curr_link_num += 1

        if curr_link_num % count_json_items == 0:
            json_vacancies = json.dumps(vacancies, ensure_ascii=False)
            loader.load(json_vacancies)
            vacancies = []

    if len(vacancies) > 0:
        json_vacancies = json.dumps(vacancies)
        loader.load(json_vacancies)