import aiohttp
import asyncio
import re
import json
from urllib.parse import urlencode
from datetime import datetime
import logging


class IndeedParser:
    def __init__(self, params=None):
        if params is None:
            params = {
                'path': "jsons/",
                'start_from': 0,
                'pages': 10,
                'json_size': 100,
                'log_path': 'logs/',
                'semaphore_count': 10,
            }
        self.params = params
        self.failed_requests_list = []
        self.vacancy_list = []
        self.keywords = ['python', 'java', 'c/c++', 'c#', 'android', 'kotlin', 'ios', 'swift', 'objective-c',
                         'rust', 'scala', 'vr/ar', 'backend', 'frontend', 'mobile', 'react', 'flutter', 'sql',
                         'teamlead', 'software engineer', 'devops', 'full stack', 'embedded', 'data science',
                         'analytics', 'system administrator', 'php', 'javascript', 'manager', 'networking',
                         'haskell', 'golang', 'typescript', 'unity', 'unreal']
        self.path = params['path']
        self.log_path = params['log_path']
        self.start_from = params['start_from']
        self.pages = params['pages']
        self.json_size = params['json_size']
        self.vacancy_count = 0
        self.semaphore_count = params['semaphore_count']
        self.logger = logging.getLogger('indeed_parser')
        self.amount_requests = len(self.keywords) * self.pages * 16
        self.config_logger()
        self.api_keys_list = []
        self.upload_api_keys()
        self.api_key = self.get_new_api_key()
        self.count_api_requests = 0

    def config_logger(self):
        text_format = '%(asctime)s::%(name)s:%(lineno)d::%(levelname)s - %(message)s'
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(text_format))
        sh.setLevel(logging.INFO)
        full_filename = f'{self.log_path}log-{datetime.now().strftime("%H-%M_%d-%m")}.log'
        fh = logging.FileHandler(filename=full_filename)
        fh.setFormatter(logging.Formatter(text_format))
        fh.setLevel(logging.INFO)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        self.logger.info('LOGGER WAS INITIALIZED')
        self.logger.info(f'LOGGER FILENAME IS {full_filename}')

    def upload_api_keys(self):
        api_key_needs = self.amount_requests//1000 + 2
        try:
            with open('api_keys.txt', 'r') as file:
                api_keys = list(filter(lambda x: len(x) > 0, file.readlines()))
                api_keys = list(map(lambda x: x.strip(), api_keys))
                api_keys_counts = len(api_keys)
                if api_keys_counts > 0 and api_key_needs <= api_keys_counts:
                    self.api_keys_list = api_keys[:api_key_needs]
                    self.logger.info(f'UPLOAD {api_key_needs} API KEYS FROM FILE')
                elif api_key_needs > api_keys_counts:
                    raise Exception('NOT ENOUGH API KEYS IN FILE')
                else:
                    raise Exception("file with API keys is empty")
        except Exception as e:
            self.logger.error(e)
        self.write_api_keys_to_file(api_keys[api_key_needs:])

    def write_api_keys_to_file(self, api_keys_list):
        try:
            with open('api_keys.txt', 'w') as file:
                api_keys_as_txt = '\n'.join(api_keys_list)
                file.write(api_keys_as_txt)
        except Exception as e:
            self.logger.error(e)

    def get_new_api_key(self):
        if len(self.api_keys_list) > 0:
            return self.api_keys_list.pop(-1)
        else:
            self.logger.error("API KEYS LIST IS EMPTY")
            return None
            
    def get_json_filename(self):
        time_now = datetime.now().strftime("%H_%M_%S-%d_%m_%Y")
        return f"indeed_{self.json_size}_{time_now}.json"

    @staticmethod
    def calculate_publish_date(days_ago, datetime_now):
        today_in_sec = int(datetime_now.timestamp())
        days_lst = re.findall(r'(\d+)', days_ago)
        if not days_lst:
            return datetime_now.strftime("%Y-%m-%d %H:%M:%S")
        days = int(days_lst[0])
        days_to_sec = days * 24 * 60 * 60
        publish_date_in_sec = today_in_sec - days_to_sec
        publish_date = datetime.fromtimestamp(publish_date_in_sec)
        return publish_date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_salary(json_blog):
        min_salary = 0
        max_salary = 0
        estimated_salary_model = json_blog["salaryGuideModel"]["estimatedSalaryModel"]
        if estimated_salary_model is not None:
            raw_min_salary = int(estimated_salary_model["min"]) if estimated_salary_model["min"] else 0
            raw_max_salary = int(estimated_salary_model["max"]) if estimated_salary_model["max"] else 0
            if estimated_salary_model.get("type") == "YEARLY":
                min_salary = raw_min_salary // 12
                max_salary = raw_max_salary // 12
            elif estimated_salary_model.get("type") == "DAILY":
                min_salary = raw_min_salary * 30
                max_salary = raw_max_salary * 30

        elif json_blog["salaryInfoModel"] is not None:
            salaty_text = json_blog["salaryInfoModel"]["salaryText"]
            salaries = re.findall(r'(\d+\.?,?\d*)', salaty_text)
            if len(salaries) == 1:
                raw_min_salary = float(salaries[0].replace(",", ""))
                raw_max_salary = raw_min_salary
            elif len(salaries) == 2:
                raw_min_salary = float(salaries[0].replace(",", ""))
                raw_max_salary = float(salaries[1].replace(",", ""))
            else:
                raw_min_salary = 0
                raw_max_salary = 0

            if 'hour' in salaty_text:
                min_salary = int(raw_min_salary * 40 * 4)
                max_salary = int(raw_max_salary * 40 * 4)
            elif 'year' in salaty_text:
                min_salary = raw_min_salary // 12
                max_salary = raw_max_salary // 12

        return min_salary, max_salary

    @staticmethod
    def match_last_try(line, keywords, ban_word=""):
        for keyword in keywords:
            if keyword in line:
                pattern = f'(<p>)?(<b>)?[<\w\s>]*?({ban_word})?[\w\s]*?{keyword}s?.?[\w\s]*?({ban_word})?.?(<\/b>)?(<\/p>)?<ul><li>(.*?)<\/li><\/ul>'
                result_raw_lst = re.findall(pattern, line)
                if not result_raw_lst:
                    continue
                i = 0
                if ban_word != "":
                    i = -1
                    for j in range(len(result_raw_lst)):
                        if ban_word not in result_raw_lst[j]:
                            i = j
                            break
                    if i < 0:
                        continue
                result = result_raw_lst[i][6].replace('</li>', '<li>').split('<li>')
                return list(map(lambda s: s.replace("</p>", "").replace("<p>", "").strip(),
                                list(filter(lambda s: s != '', result))))
        return []

    @staticmethod
    def match_first_try(line, keywords, ban_word=""):
        for keyword in keywords:
            if keyword in line:
                pattern = f'(·|-)?[<\w\s>]*?({ban_word})?[\w\s]*?{keyword}s?.?[\w\s]*?({ban_word})?.?(<\/b>)?(<\/p>)?<p>[·|-](.*?)<\/p><p>[^·-]'
                result_raw_lst = re.findall(pattern, line)
                if not result_raw_lst or result_raw_lst[0][0] == "·" or result_raw_lst[0][0] == "-":
                    continue
                i = 0
                if ban_word != "":
                    i = -1
                    for j in range(len(result_raw_lst)):
                        if ban_word not in result_raw_lst[j]:
                            i = j
                            break
                    if i < 0:
                        continue
                result = result_raw_lst[i][5].replace('</p>', '<p>').split('<p>')
                return list(map(lambda s: s.replace("· ", "").replace("- ", "").strip(),
                                list(filter(lambda s: s != '', result))))
        return []

    @staticmethod
    def parse_description(html):
        keywords = []
        for keyword in keywords:
            if keyword in html:
                description = re.findall(r'', html)
                return description
        return ""

    @staticmethod
    def parse_experience(html):
        if "experience" in html:
            left_amount = re.findall(r'(\d+).*?[years/.]\D*?experience', html)
            right_amount = re.findall(r'experience\D*?(\d+).*?[years]', html)
            exp_maybe = left_amount + right_amount
            if exp_maybe:
                filtered_lst = list(filter(lambda x: int(x) < 11, exp_maybe))
                if not filtered_lst:
                    return 0
                experience = int(max(filtered_lst, key=int))
                return experience
        return 0

    def parse_vacancy(self, html):
        description = self.parse_description(html)
        experience = self.parse_experience(html)

        necessary_keywords = ['technologies', 'skill', 'necessary', 'qualification', 'looking for', 'requirement',
                              'required', 'you’ll need', "you'll need", 'what you need', 'what skills? you need',
                              'you will need', 'experience', 'you have', 'must have']
        extra_keywords = ['preferred', 'desired', 'you also have']
        responsibilities_keywords = ['description', 'duties', 'responsibilities',
                                     "you’ll do", "you will do", "you'll do"]

        necessary_lst = self.match_first_try(html, necessary_keywords, ban_word="preferred")
        if not necessary_lst:
            necessary_lst = self.match_last_try(html, extra_keywords, ban_word="preferred")

        extra_lst = self.match_first_try(html, extra_keywords)
        if not extra_lst:
            extra_lst = self.match_last_try(html, necessary_keywords)

        responsibilities_lst = self.match_first_try(html, responsibilities_keywords)
        if not responsibilities_lst:
            responsibilities_lst = self.match_last_try(html, responsibilities_keywords)

        return {
            'description': description,
            'work_exp': experience,
            'necessary': necessary_lst,
            'extra': extra_lst,
            'responsibilities': responsibilities_lst
        }

    def parse_job(self, json_blob, job_key):
        job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
        location = json_blob["jobLocation"].split(", ")
        if len(location) > 1:
            city, country = location
        else:
            city, country = ("Remote", "Remote")
        datetime_now = datetime.now()
        days_ago = json_blob["jobMetadataFooterModel"].get("age")
        publish_time = self.calculate_publish_date(days_ago, datetime_now)
        min_salary, max_salary = self.get_salary(json_blob)
        raw_html = job.get("sanitizedJobDescription").get("content")
        description_html = re.sub(r'>\s*?<', '><', raw_html.lower().replace('<br>', '').replace("\n", ''))
        parsed_vacancy = self.parse_vacancy(description_html)
        title = job.get("jobInfoHeaderModel").get("jobTitle")
        result = {
            "parsing": {
                "date": datetime_now.strftime("%Y-%m-%d %H:%M:%S"),
                "resource": "indeed",
            },
            "company": {
                "name": job['jobInfoHeaderModel'].get('companyName'),
                "location": {
                    "country": country,
                    "city": city,
                    "street": ""
                }
            },
            "vacancy": {
                "id": job_key,
                "title": title,
                "publicDate": publish_time,
                "description": parsed_vacancy['description'],
                "workExp": {
                    "min": str(parsed_vacancy['work_exp']),
                    "max": str(parsed_vacancy['work_exp'])
                },
                "salary": {
                    "min": str(min_salary),
                    "max": str(max_salary),
                    "currency": "USD",
                    "gross": 1
                },
                "skills": {
                    "necessary": parsed_vacancy['necessary'],
                    "extra": parsed_vacancy['extra'],
                    "key": []
                },
                "responsibilities": parsed_vacancy['responsibilities']
            }
        }
        return result

    @staticmethod
    def scrapeops_url(url, api_key):
        payload = {'api_key': api_key, 'url': url, 'country': 'us'}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url

    @staticmethod
    def get_indeed_search_url(keyword, offset=0):
        parameters = {"q": keyword, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    def get_vacancies(self):
        #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.create_tasks())
        if len(self.vacancy_list) > 0:
            self.load_to_json()
        failed_requests_list_len = len(self.failed_requests_list)
        if failed_requests_list_len > 0:
            self.logger.info(f'There are {failed_requests_list_len} failed requests')
            asyncio.run(self.retry_for_failed_requests())
        if len(self.api_keys_list) > 0:
            self.write_api_keys_to_file(self.api_keys_list)

    def load_to_json(self):
        path_to_file = self.path + self.get_json_filename()
        vacancy_list_len = len(self.vacancy_list)
        self.logger.info(f'JSON FILENAME IS {path_to_file}. COUNT: {vacancy_list_len}')
        json_vacancies = json.dumps(self.vacancy_list, ensure_ascii=False)
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(json_vacancies)
        self.vacancy_list = []

    async def request_vacancy(self, session, job_key, api_key):
        try:
            vacancy_url = 'https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job_key
            proxy_vacancy_url = self.scrapeops_url(vacancy_url, api_key)
            async with session.get(proxy_vacancy_url) as response_vacancy:
                self.logger.info(f"GET VACANCY PAGE. STATUS: {response_vacancy.status}")
                if response_vacancy.status == 200:
                    html = await response_vacancy.text()
                    result = re.findall(r'_initialData=(\{.+?\});', html)
                    if len(result) > 0:
                        json_blob = json.loads(result[0])
                        vacancy = self.parse_job(json_blob, job_key)
                        self.vacancy_list.append(vacancy)
                        self.vacancy_count += 1
                        self.logger.info(f'SUCCESS! VACANCIES ON FILE: {self.vacancy_count}')
                        if self.vacancy_count == self.json_size:
                            self.load_to_json()
                            self.vacancy_count = 0
                elif response_vacancy.status == 401:
                    raise Exception('Server disconnected')
        except Exception as e:
            self.logger.error(e)
            if e == 'Server disconnected':
                self.logger.error('API KEY WAS ENDED. URL APPEND TO failed_requests_list')
                self.failed_requests_list.append(job_key)

    async def get_job_list(self, session, url, api_key, asyncio_semaphore):
        try:
            proxy_url = self.scrapeops_url(url, api_key)
            async with asyncio_semaphore:
                async with session.get(proxy_url) as response_vacancy_list:
                    self.logger.info(f"GET SEARCH PAGE WITH VACANCIES. STATUS: {response_vacancy_list.status}")
                    if response_vacancy_list.status == 200:
                        html = await response_vacancy_list.text()
                        result = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', html)
                        if len(result) > 0:
                            json_blob = json.loads(result[0])
                            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
                            for _, job in enumerate(jobs_list):
                                if job.get('jobkey') is not None:
                                    if self.count_api_requests > 999:
                                        self.api_key = self.get_new_api_key()
                                        self.count_api_requests = 0

                                    self.count_api_requests += 1
                                    await self.request_vacancy(session, job.get('jobkey'), self.api_key)
        except Exception as e:
            self.logger.error(e)

    async def retry_for_failed_requests(self):
        headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                if not self.api_key:
                    raise Exception('No api key')

                for job_key in self.failed_requests_list:
                    if self.api_key:
                        task = asyncio.create_task(self.request_vacancy(session, job_key, self.api_key))
                        tasks.append(task)
                        self.count_api_requests += 1

                        if self.count_api_requests > 999:
                            self.api_key = self.get_new_api_key()
                            self.count_api_requests = 0
                await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(e)

    async def create_tasks(self):
        asyncio_semaphore = asyncio.BoundedSemaphore(self.semaphore_count)
        headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                if not self.api_key:
                    raise Exception('No api key')

                for keyword in self.keywords:
                    for offset in range(self.start_from, self.pages*10, 10):
                        url = self.get_indeed_search_url(keyword, offset)
                        if self.api_key:
                            task = asyncio.create_task(self.get_job_list(session, url, self.api_key, asyncio_semaphore))
                            tasks.append(task)
                            self.count_api_requests += 1

                            if self.count_api_requests > 999:
                                self.api_key = self.get_new_api_key()
                                self.count_api_requests = 0
                await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(e)
