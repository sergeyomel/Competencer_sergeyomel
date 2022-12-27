import json

import requests, re
from datetime import date

from src.db.requests.DbLoader import DbLoader
from src.parsers.hh_parser.Area import Areas


class HhParser():

    def __init__(self):
        self.searcherCountry = Areas()
        self.professional_roles = ['156', '160', '10', '12', '150', '25', '165', '34', '36', '73', '155', '96', '164',
                                   '104', '157', '107', '112', '113', '148', '114', '116', '121', '124', '125', '126']
        self.specialization = '1.221'
        self.dbloader = DbLoader()

    def del_tags(self, data):
        str_symbols = ['\\r', '\\n','</li>']

        for i in str_symbols:
            if i == '</li>':
                data = data.replace(i,';')
            elif i == '\\n':
                data = data.replace(i, ' ')
            elif i == '\\r':
                data = data.replace(i,'')

        data = re.sub(r'(?<=<).+?(?=>)', '', data).replace('<>', '')
        return data

    def del_comma_in_list(self, data):
        new_list = []
        for i in data:
            if i == "":
                continue
            if i[1] == '-' or i[0] == ':':
                i = i[2:]
            i = re.sub(r'\s{2,}'," ", i)
            if i[-1] == ',' or i[-1] == '.' or i[-1] == ';':
                new_list.append(i[:-1])

            else:
                new_list.append(i)

        return new_list

    def vacancy_parse(self, data):

        id = re.search(r'\d+', data)[0]

        name = re.search(r'(?<=:).+',re.search(r'\],\s*"name":\s*.+?(?=,\s*")',data)[0])[0].replace('"','')

        try:
            salary = re.findall(r'\d+', re.search(r'"salary"\s*.+?(?=,\s*"type)', data)[0])
            if len(salary) > 1:
                min_salary = salary[0]
                max_salary = salary[1]
            else:
                min_salary = salary[0]
                max_salary = '0'
        except:
            min_salary = '0'
            max_salary = '0'

        try:
            experience = re.findall(r'\d+',re.search(r'"experience".+?(?=\s*})',data)[0])
            if len(experience)>1:
                min_exp = experience[0]
                max_exp = experience[1]
            else:
                min_exp = experience[0]
                max_exp = min_exp
        except:
            min_exp = '0'
            max_exp = '0'

        try:
            description = re.sub(r'"description":\s*"','',re.search(r'(?<="contacts":\s*\w{4},\s*)"description":\s*".*?(?=(Обязанности|Задачи|Требования|Условия|",))',data, flags=re.IGNORECASE)[0])
            description = self.del_tags(description)
            if len(description) == 0:
                description = []
        except:
            description = []

        try:
            requirements = re.search(r'(?<=:).+',re.search(r'(?<=Требования).*?(?=(Обязанности|Условия|Задачи|",))', data,flags=re.IGNORECASE)[0])[0]
            requirements = self.del_tags(requirements).split(';')
            requirements = self.del_comma_in_list(requirements)
            del requirements[-1]
        except:
            requirements = []

        try:
            responsibilities = re.search(r'(?<=:).+', re.search(r'((?<=Обязанности)|(?<=Задачи)).*?(?=(Условия|Требования|",))', data,flags=re.IGNORECASE)[0])[0]
            responsibilities = self.del_tags(responsibilities).split(';')
            responsibilities = self.del_comma_in_list(responsibilities)
            del responsibilities[-1]

        except:
            responsibilities = []

        try:
            additional_skills = re.search(r'((?<=Дополнительные навыки)|(?<=Дополнительные)|(?<=\\nнавыки)|(?<=Будет плюсом)|(?<=Дополнительные требования)|(?<=Дополнительные\\nтребования)).+?(?=(Условия|Требования|",))', data,flags=re.IGNORECASE)[0]
            additional_skills = self.del_tags(additional_skills).split(';')
            additional_skills = self.del_comma_in_list(additional_skills)
            del additional_skills[-1]
        except:
            additional_skills = []


        key_skills = re.search(r'key_skills":\s*.*?(?=\s*],\s*")', data)[0]
        if key_skills == '[':
            list_of_key_skills = []
        else:
            key_skills = re.findall(r'"name":\s*"\w+"',key_skills)
            list_of_key_skills = []
            for i in key_skills:
                i = i.split(':')[1].replace('"','')
                list_of_key_skills.append(i)

        try:
            country = re.search(r'area":\s*.+?(?=,\s*")',data)[0].split(':')[2].replace('"','').replace(' ', '')
            country = self.searcherCountry.get_country_name(country)
        except:
            country = ''

        try:
            city = re.search(r'"city":\s*.+?(?=\s*,)', data)[0].split(':')[1].replace('"', '')
        except:
            city = ''

        try:
            street = re.search(r'"street":\s*.+?(?=\s*,)', data)[0].split(':')[1].replace('"', '')
        except:
            street = ''


        employer = re.search(r'"name":\s*.+?(?=,\s*")', re.search(r'employer":\s*.+?(?=trusted)', data)[0])[0].split(':')[1].replace('"', '')

        published = re.search(r'published_at":\s*.+?(?=T)', data)[0].split(':')[1].replace('"', '')

        date_of_parsing = str(date.today())

        item = {
          "parsing": {
            "date": date_of_parsing,
            "resource": "hh"
          },
          "company": {
            "name": employer,
            "location": {
              "country": country,
              "city": city,
              "street": street
            }
          },
          "vacancy": {
            "id": id,
            "title": name,
            "publicDate": published,
            "description": description,
            "workExp": {
                "min": min_exp,
                "max": max_exp
            },
            "salary": {
              "min": min_salary,
              "max": max_salary
            },
            "skills": {
              "necessary": requirements,
              "extra": additional_skills,
              "key": list_of_key_skills
            },
            "responsibilities": responsibilities
          }
        }
        return item

    def get_data(self, id):
        url = f'https://api.hh.ru/vacancies/{id}'
        req = requests.get(url)
        data = req.content.decode()
        req.close()
        return data

    def get_vacancy_json(self, json_data):

        vacancies = []

        for json_item in json_data:
            txt_item_data = json.dumps(json_item, ensure_ascii=False)
            try:
                vacancy_specialization = re.search(r'"specializations":\s\[{"id":\s".+?(?=,)', txt_item_data)[0].split(':')[2].replace('"','').replace(' ', '')
                vacancy_professional = re.search(r'"professional_roles":\s*\[{"id":\s*"\d+', txt_item_data)[0].split(':')[2].replace('"','').replace(' ', '')
            except:
                continue

            if vacancy_professional in self.professional_roles or vacancy_specialization == self.specialization:
                vacancy = self.vacancy_parse(txt_item_data)
                vacancies.append(vacancy)

        return vacancies