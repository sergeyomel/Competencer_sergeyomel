import json

from src.db.requests.CompanyJSONGroup.CompanyLocationsTable import CompanyLocationsTable
from src.db.requests.ParsingsJSONGroup.ParserTable import ParserTable


# Класс для загрузки json объектов в БД.
# Принимает на вход список из JSON объектов, описывающих вакансию
class DbLoader:

    def __init__(self, host, user, password, db_name):
        self.company_locations = CompanyLocationsTable(host, user, password, db_name)
        self.parsers_table = ParserTable(host, user, password, db_name)

    def load(self, data):
        data = json.loads(data)

        for item in data:
            self.company_locations.insert(item['company'])
            self.parsers_table.insert(item)

