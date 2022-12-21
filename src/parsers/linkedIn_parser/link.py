import random
import time
import json
import re
import fake_useragent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Parser():
    def __init__(self):
        self.login = ''
        self.password = ''
        self.current_link_value = 1
        self.html_elements = []
        self.job_id = []
        self.parsed_ids = []
        self.chrome_options = Options()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.ban_boolean = False
        self.job_url = 'https://www.linkedin.com/jobs/view/'
        self.url_with_filter = None
        self.curl = None
        self.t = time.localtime()

    def set_urls(self):
        try:
            with open('url_with_filter.txt', 'r', encoding='utf-8') as f:
                self.url_with_filter = f.readlines()
        except Exception as error:
            print(error)

    def set_login_info(self):
        try:
            with open('login.txt', 'r', encoding="utf-8") as f:
                lines = f.readlines()
                self.login = lines[0]
                self.password = lines[1]
        except Exception as error:
            print(error)

    def set_old_ids(self):
        try:
            with open('linkedin.json', encoding='utf-8') as file:
                data = json.loads(file.read())
            for ID in data:
                self.parsed_ids.append(ID['parsing']['id'])
        except Exception as error:
            print(error, 'set_old_id')

    def auth(self):
        try:
            self.driver.get('https://www.linkedin.com/checkpoint/lg/sign-in-another-account')
            login_field = self.driver.find_element(By.ID, 'username')
            password_field = self.driver.find_element(By.ID, 'password')

            login_field.send_keys(self.login)
            password_field.send_keys(self.password)

            self.driver.find_element(By.CLASS_NAME, 'from__button--floating').click()

            self.ban_boolean = False
            self.t = time.localtime()
            print(f'Auth complete. Time: {time.strftime("%H:%M:%S", self.t)}')
            time.sleep(random.randint(1, 2))
        except Exception as error:
            self.auth()
            print(error, 'auth')

    def get_current_url(self, url):
        try:
            self.driver.get(url)
            elements = self.driver.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
            ban = self.driver.find_element(By.CLASS_NAME, 'jobs-search-no-results-banner__image')
            if ban:
                self.ban_boolean = True
                return
            for element in elements:
                temp = element.get_attribute('data-occludable-job-id')
                if temp in self.job_id or temp in self.parsed_ids:
                    continue
                else:
                    self.job_id.append(temp)

            self.t = time.localtime()
            print(f'Url: {url} get ID\'s. Time: {time.strftime("%H:%M:%S", self.t)}')

            self.driver.find_element(By.CSS_SELECTOR, f"[aria-label='Page {self.current_link_value + 1}'").click()
            self.current_link_value += 1
            time.sleep(random.randint(1, 2))
            self.curl = self.driver.current_url
        except Exception as error:
            self.get_current_url(url)
            print(error, 'get_current_url')

    def get_data_from_link(self, job_id, ids):
        try:
            user = fake_useragent.UserAgent()
            data = requests.get(
                url=self.job_url + str(job_id),
                headers={'user-agent': user.random}
            )
            self.t = time.localtime()
            if data.status_code == 200:
                soup = BeautifulSoup(data.content, 'lxml')
                self.html_elements.append(
                    {
                        'parsing': {
                            'date': time.strftime("%H:%M:%S", self.t),
                            'resource': 'LinkedIn',
                            'id': job_id
                        },
                        'company': {
                            'name': re.sub(r'\s+', ' ', soup.find('a', {'class': 'topcard__org-name-link'}).text.replace('\n', '')),
                            'location': re.sub(r'\s+', ' ', soup.find('span', {'class': 'topcard__flavor--bullet'}).text.replace('\n', ''))
                        },
                        'vacancy': {
                            'title': re.sub(r'\s+', ' ', soup.find('h1', {'class': 'top-card-layout__title'}).text.replace('\n','')),
                            'publicDate': re.sub(r'\s+', ' ', soup.find('span', {'class': 'posted-time-ago__text'}).text.replace('\n', '')),
                            'description': soup.find('div', {'class', 'show-more-less-html__markup'}).text.replace('\n',' ')
                        },
                        'skills': {
                            'List of Job Criteris': [re.sub(r'\s+', ' ',criteris.text.replace('\n', ' ')) for criteris in soup.find_all('span', {'class', 'description__job-criteria-text--criteria'})],
                        },
                        'responsibilities': {
                            '': ''
                        }
                    }
                )

                self.t = time.localtime()
                print(f'#{ids}, {job_id} complete. Time: {time.strftime("%H:%M:%S", self.t)}')

            elif data.status_code == 429:
                print('Status code: ', data.status_code)
                time.sleep(random.randint(10, 20))
                self.get_data_from_link(job_id, ids)
            else:
                print('Status code: ', data.status_code)
                time.sleep(random.randint(3, 5))
                self.get_data_from_link(job_id, ids)

        except Exception as error:
            time.sleep(random.randint(3, 5))
            self.get_data_from_link(job_id, ids)
            print(error, 'get_data_from_link')


def LinkedIn():
    p = Parser()
    print(f'Start: {time.strftime("%H:%M:%S", p.t)}')
    p.set_login_info()
    p.set_urls()
    p.set_old_ids()
    p.auth()
    for url in p.url_with_filter:
        p.curl = url
        for i in range(1, 40):
            if p.current_link_value != 41:
                p.get_current_url(url=p.curl)
            else:
                break
            if p.ban_boolean:
                break

        if p.ban_boolean:
            flag = input('Account was banned. Continue? [Y/N]')
            if flag == 'Y':
                p.driver.get('https://www.linkedin.com/m/logout/')
                print('Change VPN connection and account.')
                p.login = input('New login: ')
                p.password = input('New password: ')
                p.auth()
            elif flag == 'N':
                break
            else:
                continue

        p.current_link_value = 1

    p.driver.quit()

    try:
        with open('linkedin.json', encoding='utf-8') as file:
            p.html_elements = json.loads(file.read())
    except Exception as error:
        print(error)

    ids = 0
    for id in p.job_id:
        p.get_data_from_link(id, ids)
        ids += 1

    with open('linkedin.json', 'w', encoding='utf-8') as file:
        json.dump(p.html_elements, file, indent=4, ensure_ascii=False)

    print(f'Finish: {time.strftime("%H:%M:%S", p.t)}')

    return p.html_elements


if __name__ == "__main__":
    LinkedIn()
