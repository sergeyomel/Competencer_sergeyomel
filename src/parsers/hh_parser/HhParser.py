import json, re
from datetime import date

from src.db.requests.DbLoader import DbLoader
from src.parsers.hh_parser.Area import Areas
from DataHandler import DataHandler
import config

class HhParser():

    def __init__(self):
        self.searcherCountry = Areas()

    def get_salary(self, data):
        json_item =  {
                'min': '0',
                'max': '0',
                'currency': None,
                'gross': None
                }

        if data is not None:
            if data['from'] is not None:
                json_item['min'] = str(data['from'])
            if data['to'] is not None:
                json_item['max'] = str(data['to'])
            if data['currency'] is not None:
                json_item['currency'] = data['currency']
            if data['gross'] is not None:
                json_item['gross'] = str(data['gross'])

        return json_item


    def get_experience(self, data):
        min = '0'
        max = '0'

        if data is not None:
            experience = re.findall(r'\d+', data)
            if len(experience)>1:
                min = experience[0]
                max = experience[1]
            elif len(experience) == 1:
                min = experience[0]
                max = min

        return {
                "min": min,
                "max": max
               }

    def get_description(self, data):
        try:
            description = re.search(r'.*?(?=(Обязанности|Задачи|Требования|Условия|Мы ожидаем от Вас|",))',data, flags=re.IGNORECASE)[0]
            description = DataHandler.del_tags(description)
            if len(description) > 0:
                for index in range(len(description)):
                    if len(description[index]) > 1000:
                        description[index] = description[index][:1000]
            if len(description) == 0:
                description = ""
        except:
            description = ""

        return description

    def get_requirements(self, data):
        try:
            requirements = re.search(r'((?<=Требования)|(?<=Мы ожидаем от Вас)|(?<=Чем предстоит заниматься)).*?(?=(Обязанности|Условия|Задачи|Мы предлагаем|",))', data,flags=re.IGNORECASE)[0]
            requirements = DataHandler.del_tags(requirements).split(';')
            requirements = DataHandler.del_comma_in_list(requirements)
            del requirements[-1]
        except:
            requirements = ""

        return requirements

    def get_additional_skills(self, data):
        try:
            additional_skills = re.search(r'((?<=Дополнительные навыки)|(?<=Дополнительные)|(?<=\\nнавыки)|(?<=Будет плюсом)|(?<=Дополнительные требования)|(?<=Дополнительные\\nтребования)).+?(?=(Условия|Требования|",))', data,flags=re.IGNORECASE)[0]
            additional_skills = DataHandler.del_tags(additional_skills).split(';')
            additional_skills = DataHandler.del_comma_in_list(additional_skills)
            del additional_skills[-1]
        except:
            additional_skills = ""

        return additional_skills

    def get_responsibilities(self, data):
        try:
            responsibilities = re.search(r'(?<=:).+', re.search(r'((?<=Обязанности)|(?<=Задачи)).*?(?=(Условия|Требования|",))', data,flags=re.IGNORECASE)[0])[0]
            responsibilities = DataHandler.del_tags(responsibilities).split(';')
            responsibilities = DataHandler.del_comma_in_list(responsibilities)
        except:
            responsibilities = ""

        return responsibilities

    def get_key_skills(self, data):
        if data is None:
            return []

        skills = []
        if len(data) > 0:
            for item in data:
                skills.append(item['name'])

        return skills

    def get_location(self, data):
        country = data['area']['id']
        country = self.searcherCountry.get_country_name(country)

        city = ''
        street = ''
        if data['address'] is not None:
            if data['address']['city'] is not None:
                city = data['address']['city']
            if data['address']['street'] is not None:
                street = data['address']['street']

        return {
                  "country": country,
                  "city": city,
                  "street": street
               }

    def vacancy_parse(self, data):

        id = data['id']
        name = data['name']
        employer = data['employer']['name']
        published = data['published_at'].replace('T', ' ')
        date_of_parsing = str(date.today())

        experience = self.get_experience(data['experience']['name'])
        salary = self.get_salary(data['salary'])
        description_hh = data['description']
        description = self.get_description(description_hh)
        requirements = self.get_requirements(description_hh)
        additional_skills = self.get_additional_skills(data)
        responsibilities = self.get_responsibilities(description_hh)
        key_skills = self.get_key_skills(data['key_skills'])
        location = self.get_location(data)

        item = {
          "parsing": {
            "date": date_of_parsing,
            "resource": "hh"
          },
          "company": {
            "name": employer,
            "location": location
          },
          "vacancy": {
            "id": id,
            "title": name,
            "publicDate": published,
            "description": description,
            "workExp": experience,
            "salary": salary,
            "skills": {
              "necessary": requirements,
              "extra": additional_skills,
              "key": key_skills
            },
            "responsibilities": responsibilities
          }
        }
        return item

    def get_vacancy_json(self, json_data):

        vacancies = []

        for json_item in json_data:
            vacancy_specialization = json_item['specializations']
            vacancy_specialization = None if len(vacancy_specialization) == 0 else vacancy_specialization[0]['id']

            vacancy_professional = json_item['professional_roles']
            vacancy_professional = None if len(vacancy_professional) == 0 else vacancy_professional[0]['id']

            if vacancy_specialization is None and vacancy_professional is None:
                continue

            if vacancy_professional in config.professional_roles or vacancy_specialization == config.specialization:
                vacancy = self.vacancy_parse(json_item)
                vacancies.append(vacancy)

        return vacancies