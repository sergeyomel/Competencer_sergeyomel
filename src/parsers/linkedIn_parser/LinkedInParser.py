from DictGrabber import DictGrabber
from VacancyParser import VacancyParser
from data.config import *
import asyncio
import json
import time
import logging


def linkedin():
    try:
        logging.basicConfig(filename='main',
                            filemode='a',
                            format='%(asctime)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        grabber = DictGrabber()
        parser = VacancyParser()

        key = (element for element in keywords)

        for k in key:
            dicts_for_parse = grabber.dict_grabber(keywords=k,
                                                   location_name=location_name,
                                                   listed_at=listed_at,
                                                   limit=-1)

            asyncio.run(parser.task_gather(dicts_for_parse))

        with open('data/ParsedIds.json', 'w', encoding='utf-8') as file:
            json.dump(parser.old_ids, file)

        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        with open(f'data/parse_{current_time}.json', 'w', encoding='utf-8') as file:
            json.dump(parser.vanancy_data, file, indent=4, ensure_ascii=False)

    except Exception as Error:
        logging.exception(Error)


linkedin()
