import re
import json
import scrapy
from urllib.parse import urlencode
from datetime import datetime


class IndeedJobSpider(scrapy.Spider):
    name = "indeed_jobs"
    custom_settings = {
        'FEEDS': {'results/indeed_%(time)s.json': {'format': 'json', }}
    }

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        keyword_list = ['python', 'java', 'c/c++', 'c#', 'android', 'kotlin', 'ios', 'swift', 'objective-c',
                        'rust', 'scala', 'vr/ar', 'backend', 'frontend', 'mobile', 'react', 'flutter', 'sql',
                        'teamlead', 'software engineer', 'devops', 'full stack', 'embedded', 'data science',
                        'analytics', 'system administrator', 'php', 'javascript', 'manager', 'networking',
                        'haskell', 'golang', 'typescript', 'unity', 'unreal']
        location = ''
        for keyword in keyword_list:
            indeed_jobs_url = self.get_indeed_search_url(keyword, location)
            yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results,
                                 meta={'keyword': keyword, 'location': location, 'offset': 0})

    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        offset = response.meta['offset']
        script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_list):
                if job.get('jobkey') is not None:
                    job_url = 'https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    yield scrapy.Request(url=job_url,
                                         callback=self.parse_job,
                                         meta={
                                             'keyword': keyword,
                                             'location': location,
                                             'page': round(offset / 10) + 1 if offset > 0 else 1,
                                             'position': index,
                                             'jobKey': job.get('jobkey'),
                                         })

            # Paginate Through Jobs Pages
            if offset == 0:
                meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
                num_results = sum(category["jobCount"] for category in meta_data)
                if num_results > 1000:
                    num_results = 50

                for offset in range(10, num_results + 10, 10):
                    url = self.get_indeed_search_url(keyword, location, offset)
                    yield scrapy.Request(url=url, callback=self.parse_search_results,
                                         meta={'keyword': keyword, 'location': location, 'offset': offset})

    def calculate_publish_date(self, days_ago, datetime_now):
        today_in_sec = int(datetime_now.timestamp())
        days_lst = re.findall(r'(\d+)', days_ago)
        if not days_lst:
            return datetime_now.strftime("%Y%m%d%H%M%S")
        days = int(days_lst[0])
        days_to_sec = days*24*60*60
        publish_date_in_sec = today_in_sec - days_to_sec
        publish_date = datetime.fromtimestamp(publish_date_in_sec)
        return publish_date.strftime("%Y%m%d%H%M%S")

    def get_salary(self, json_blog):
        min_salary = 0
        max_salary = 0
        estimated_slary_model = json_blog["salaryGuideModel"]["estimatedSalaryModel"]
        if estimated_slary_model is not None:
            raw_min_salary = int(estimated_slary_model["min"]) if estimated_slary_model["min"] else 0
            raw_max_salary = int(estimated_slary_model["max"]) if estimated_slary_model["max"] else 0
            if estimated_slary_model.get("type") == "YEARLY":
                min_salary = raw_min_salary // 12
                max_salary = raw_max_salary // 12
            elif estimated_slary_model.get("type") == "DAILY":
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

    def match_last_try(self, line, keywords, ban_word=""):
        for keyword in keywords:
            if keyword in line:
                pattern = f'(<p>)?(<b>)?[<\w\s>]*?({ban_word})?[\w\s]*?{keyword}.?[\w\s]*?({ban_word})?.?(<\/b>)?(<\/p>)?<ul><li>(.*?)<\/li><\/ul>'
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
                return list(map(lambda s: s.strip(), list(filter(lambda s: s != '', result))))
        return []

    def match_first_try(self, line, keywords, ban_word=""):
        for keyword in keywords:
            if keyword in line:
                pattern = f'(·|-)?[<\w\s>]*?({ban_word})?[\w\s]*?{keyword}.?[\w\s]*?({ban_word})?.?(<\/b>)?(<\/p>)?<p>[·|-](.*?)<\/p><p>[^·-]'
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

    def parse_description(self, html):
        keywords = []
        for keyword in keywords:
            if keyword in html:
                description = re.findall(r'', html)
                return description
        return ""

    def parse_experience(self, html):
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
        responsibilities_keywords = ['description', 'duties', 'responsibilities', "you’ll do", "you will do", "you'll do"]

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

    def parse_job(self, response):
        script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
            location = json_blob["jobLocation"]
            if location != "Remote" or len(location.split(", ")) > 1:
                city, country = location.split(", ")
            else:
                city, country = ("Remote", "Remote")
            datetime_now = datetime.now()
            days_ago = json_blob["jobMetadataFooterModel"].get("age")
            publish_time = self.calculate_publish_date(days_ago, datetime_now)
            min_salary, max_salary = self.get_salary(json_blob)
            raw_html = job.get("sanitizedJobDescription").get("content")
            description_html = re.sub(r'>\s*?<', '><', raw_html.lower().replace('<br>', '').replace("\n", ''))
            parsed_vacancy = self.parse_vacancy(description_html)
            result = {
                "parsing": {
                    "date": datetime_now.strftime("%Y%m%d%H%M%S"),
                    "resource": "indeed",
                    "id": response.meta['jobKey'],
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
                    "publicDate": publish_time,
                    "description": parsed_vacancy['description'],
                    "workExp": parsed_vacancy['work_exp'],
                    "wage": {
                        "min": min_salary,
                        "max": max_salary
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


