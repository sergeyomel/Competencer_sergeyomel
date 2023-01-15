import time
from datetime import timedelta, datetime
import re
import logging
import fake_useragent
import requests
from bs4 import BeautifulSoup
from data.config import job_url

class VacancyParser:
    def __init__(self):
        self.t = time.localtime()
        self.ban_words = ['</ul>', '<strong>', '<u>', '</span>', '</div>', '<br/><br/>']

    def matching_ul(self, keyword, text):
        try:
            pattern = f'{keyword}.+?(<ul>.+?)</ul>'
            temp = re.sub('<li>|</li>|<ul>|</ul>|<br/>', '^',
                          re.findall(pattern, text.lower(), re.M | re.S)[0]).split('^')
            return [e.replace('&amp', '') for e in temp if e]
        except Exception as Error:
            logging.exception(Error)

    def vacancy_parse(self, job_id):
        try:
            user = fake_useragent.UserAgent()
            data = requests.get(
                url=job_url + job_id,
                headers={'user-agent': user.random}
            )
            self.t = time.localtime()
            if data.status_code == 200:
                soup = BeautifulSoup(data.content, 'lxml')

                full_vacancy_description = soup.find('div', {'class', 'show-more-less-html__markup'})

                try:
                    name = re.sub(r'\s+', ' ',
                                  soup.find('a', {'class': 'topcard__org-name-link'}).
                                  text.replace('\n', ''))
                except Exception as Error:
                    logging.exception(Error)
                    name = ''

                try:
                    location = re.sub(r'\s+', ' ',
                                      soup.find('span', {'class': 'topcard__flavor--bullet'}).
                                      text.replace('\n', ''))
                except Exception as Error:
                    logging.exception(Error)
                    location = ''

                try:
                    title = re.sub(r'\s+', ' ',
                                   soup.find('h1', {'class': 'top-card-layout__title'}).
                                   text.replace('\n',''))
                except Exception as Error:
                    logging.exception(Error)
                    title = ''

                try:
                    text_time = re.sub(r'\s+', ' ',
                                       soup.find('span', {'class': 'posted-time-ago__text'}).
                                       text.replace('\n', ''))
                    now = datetime.now()
                    if 'minute' in text_time:
                        temp = float(re.findall('\d+', text_time)[0])
                        public_date = (now - timedelta(minutes=temp)).strftime("%Y-%m-%d %H:%M:%S")
                    elif 'hour' in text_time:
                        temp = float(re.findall('\d+', text_time)[0])
                        public_date = (now - timedelta(hours=temp)).strftime("%Y-%m-%d %H:%M:%S")
                    elif 'day' in text_time:
                        temp = float(re.findall('\d+', text_time)[0])
                        public_date = (now - timedelta(days=temp)).strftime("%Y-%m-%d %H:%M:%S")
                    elif 'week' in text_time:
                        temp = float(re.findall('\d+', text_time)[0])
                        public_date = (now - timedelta(weeks=temp)).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        public_date = (now).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as Error:
                    logging.exception(Error)
                    public_date = ''

                try:
                    description = ''
                except Exception as Error:
                    logging.exception(Error)
                    description = ''

                try:
                    skills_keyword = 'skills'
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
                    responsibilities = self.matching_ul(responsibilities_keyword, str(full_vacancy_description))
                    if responsibilities is None:
                        responsibilities = []
                except Exception as Error:
                    logging.exception(Error)
                    responsibilities = []

                if not skills and not responsibilities:
                    return 0

                result = {
                    'parsing': {
                        'date': time.strftime("%Y-%m-%d %H:%M:%S", self.t),
                        'resource': 'LinkedIn',
                        'id': job_id
                    },
                    'company': {
                        'name': name,
                        'location': location
                    },
                    'vacancy': {
                        'title': title,
                        'publicDate': public_date,
                        'description': description
                    },
                    'skills': {
                        'skills': skills,
                        'extra': extra
                    },
                    'responsibilities': responsibilities
                }
                return result
        except Exception as Error:
            logging.exception(Error)