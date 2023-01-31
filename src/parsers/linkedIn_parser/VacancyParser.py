import time
import re
import logging
import fake_useragent
import datetime
from bs4 import BeautifulSoup
from data.config import job_url
from data.config import industryIDs
import asyncio
import aiohttp
import json

class VacancyParser:
    def __init__(self):
        self.t = time.localtime()
        self.ban_words = ['</ul>', '<strong>', '<u>', '</span>', '</div>', '<br/><br/>']
        self.vanancy_data = []
        self.old_ids = self.set_old_ids()
        logging.basicConfig(filename='VacancyParser',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    def set_old_ids(self):
        with open('data/ParsedIds.json', encoding='utf-8') as file:
            return json.loads(file.read())

    def matching_ul(self, keyword, text):
        try:
            pattern = f'{keyword}.+?(<ul>.+?)</ul>'
            find = re.findall(pattern, text.lower(), re.M | re.S)
            if find:
                temp = re.sub('<li>|</li>|<ul>|</ul>|<br/>|'
                              '<span>|</span>|<div>|</div>|'
                              '<strong>|</strong>', '^',
                              find[0]).split('^')
                return [e.replace('&amp', '') for e in temp if e]
        except Exception as Error:
            logging.exception(Error)

    async def task_gather(self, dicts_for_parse):
        try:
            async with aiohttp.ClientSession() as session:
                user = fake_useragent.UserAgent()
                tasks = []
                for dict_for_parse in dicts_for_parse:
                    if dict_for_parse['id'] in self.old_ids:
                        continue
                    else:
                        tasks.append(asyncio.ensure_future(self.vacancy_parser(dict_for_parse, session, user)))
                        self.old_ids.append(dict_for_parse['id'])

                await asyncio.gather(*tasks)
        except Exception as Error:
            logging.exception(Error)

    async def vacancy_parser(self, job_dict, session, user):
        try:
            async with session.get(url=job_url + job_dict['id'], headers={'user-agent': user.random}) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'lxml')

                if re.findall(f"name=.industryIds. content=.(\d+).", response_text)[0] in industryIDs:

                    full_vacancy_description = soup.find('div', {'class', 'show-more-less-html__markup'})

                    try:
                        name = re.sub(r'\s+', ' ',
                                      soup.find('a', {'class': 'topcard__org-name-link'}).
                                      text.replace('\n', ''))
                    except Exception as Error:
                        logging.exception(Error)
                        name = ''

                    try:
                        description = ''
                    except Exception as Error:
                        logging.exception(Error)
                        description = ''

                    try:
                        skills_keyword = 'skills|requirements|qualifications'
                        skills = self.matching_ul(skills_keyword, str(full_vacancy_description))
                        if skills is None:
                            skills = []
                    except Exception as Error:
                        logging.exception(Error)
                        skills = []

                    try:
                        extra_keyword = 'extra'
                        extra = self.matching_ul(extra_keyword, str(full_vacancy_description))
                        if extra is None:
                            extra = []
                    except Exception as Error:
                        logging.exception(Error)
                        extra = []

                    try:
                        responsibilities_keyword = 'responsibilities'
                        responsibilities = self.matching_ul(responsibilities_keyword,
                                                            str(full_vacancy_description))
                        if responsibilities is None:
                            responsibilities = []
                    except Exception as Error:
                        logging.exception(Error)
                        responsibilities = []

                    if not skills and not responsibilities:
                        return 0

                    self.vanancy_data.append({
                        "parsing": {
                            "date": time.strftime("%Y-%m-%d %H:%M:%S", self.t),
                            "resource": 'linkedin'
                        },
                        "company": {
                            "name": name,
                            "location": {
                                "country": "United States",
                                "city": job_dict['location'],
                                "street": ""
                            }
                        },
                        "vacancy": {
                            "id": job_dict['id'],
                            "title": job_dict['title'],
                            "publicDate": str(datetime.datetime.fromtimestamp(job_dict['listedAt'] / 1e3)),
                            "description": description,
                            "workExp": {
                                'min': '0',
                                'max': '0'
                            },
                            "salary": {
                                "min": job_dict['minSalary'],
                                "max": job_dict['maxSalary']
                            },
                            "skills": {
                                "necessary": skills,
                                "extra": extra,
                                "key": []
                            },
                            "responsibilities": responsibilities
                        }
                    })
        except Exception as Error:
            logging.exception(Error)
