import random
import time
import json
import re
import fake_useragent
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.start = 0
        self.step = 25
        self.html_elements = []
        self.links = []
        self.main_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?trk=guest_homepage-basic_guest_nav_menu_jobs&start='

    def generate_url(self, url):
        return url + str(self.start)

    def set_links_from_one_page(self, url):
        try:
            user = fake_useragent.UserAgent()
            data = requests.get(
                url=url,
                headers={'user-agent': user.random}
            )
            if data.status_code == 200:
                soup = BeautifulSoup(data.content, 'lxml')
                for a in soup.find_all('a', {'class': 'base-card__full-link'}):
                    self.links.append(a.attrs['href'])
            elif data.status_code == 429:
                print(data.status_code)
                time.sleep(random.randint(30, 60))
                self.set_links_from_one_page(url)
            else:
                print(data.status_code)
                time.sleep(random.randint(30, 60))
                self.set_links_from_one_page(url)
        except Exception as error:
            print(error, ' set')

    def get_data_from_link(self, url):
        try:
            user = fake_useragent.UserAgent()
            data = requests.get(
                url=url,
                headers={'user-agent': user.random}
            )

            if data.status_code == 200:
                soup = BeautifulSoup(data.content, 'lxml')
                self.html_elements.append(
                    {
                        'Job Name': re.sub(r'\s+', ' ', soup.find('h1', {'class': 'top-card-layout__title'}).text.replace('\n', '')),
                        'Org. Name': re.sub(r'\s+', ' ', soup.find('a', {'class': 'topcard__org-name-link'}).text.replace('\n', '')),
                        'Org. City': re.sub(r'\s+', ' ', soup.find('span', {'class': 'topcard__flavor--bullet'}).text.replace('\n', '')),
                        'Posted Time': re.sub(r'\s+', ' ', soup.find('span', {'class': 'posted-time-ago__text'}).text.replace('\n', '')),
                        'List of Job Criteris': [re.sub(r'\s+', ' ',criteris.text.replace('\n', ' ')) for criteris in soup.find_all('span', {'class', 'description__job-criteria-text--criteria'})],
                        'Full Description': soup.find('div', {'class', 'show-more-less-html__markup'}).text.replace('\n', ' ')
                    }
                )
                #print(self.html_elements[-1])
            elif data.status_code == 429:
                print(data.status_code)
                time.sleep(random.randint(30, 60))
                self.get_data_from_link(url)
            else:
                print(data.status_code)
                time.sleep(random.randint(30, 60))
                self.get_data_from_link(url)

        except Exception as error:
            print(error, ' get')

def main():
    p = Parser()
    for i in range(0, 1): # 0 , 25 , 50, 75 -> 1000:max => (0, 39)
        p.set_links_from_one_page(url=p.generate_url(p.main_url))
        p.start += p.step
        time.sleep(random.randint(30, 60))
    for l in p.links:
        p.get_data_from_link(l)
        time.sleep(random.randint(3, 15))

    with open("data.json", "a", encoding="utf-8") as file:
        json.dump(p.html_elements, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
