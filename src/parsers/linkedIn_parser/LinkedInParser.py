from IdGrabber import IdGrabber
from VacancyParser import VacancyParser
from data.config import *
import json
import logging

def set_old_ids():
    with open('data/ParsedIds.json', encoding='utf-8') as file:
        return json.loads(file.read())

def linkedin():
    try:
        grabber = IdGrabber()
        parser = VacancyParser()

        old_ids = set_old_ids()

        key = (element for element in keywords)

        current_parse_json = []
        ids_for_parse = []

        for k in key:
            print('startim new key')
            ids_for_parse += grabber.id_grabber(keywords=k,
                               industries=industries,
                               location_name=location_name,
                               listed_at=listed_at,
                               limit=-1)

            print('idi sobrani')
            id_count = 0
            for id in ids_for_parse:
                print('id #', id_count)
                id_count += 1
                if id not in old_ids:
                    temp = parser.vacancy_parse(id)
                    old_ids.append(id)
                    if temp == 0 or temp is None:
                        continue
                    else:
                        current_parse_json.append(temp)
                        print('CPJ: ', temp)
                else:
                    continue

            with open('data/ParsedIds.json', 'w', encoding='utf-8') as file:
                json.dump(old_ids, file)
            with open('data/test.json', 'w', encoding='utf-8') as file:
                json.dump(current_parse_json, file, indent=4, ensure_ascii=False)

    except Exception as Error:
        logging.exception(Error)

linkedin()