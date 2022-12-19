import logging

import psycopg2

from src.db.requests.VacancyJSONGroup.CompanyVacanciesTable import CompanyVacanciesTable
from src.db.requests.Writer import Writer

#Класс для вставки значений в таблицу parsings на основе данных из json объекта
class ParserTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)
        self.company_vacancy_table = CompanyVacanciesTable(connection)

    def insert(self, data):
        parsing_date = data['parsing']['date']
        resource_title = data['parsing']['resource']

        company_vacancy_id = self.company_vacancy_table.insert(data)

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                f"SELECT resource_id FROM resources WHERE title = '{resource_title}'"
            )
            resource_id = cursor.fetchone()[0]
            cursor.execute(
                f" INSERT INTO parsings (resource_parsing_id, parsing_date, company_vacancy_id) "
                f" VALUES ('{resource_id}', '{parsing_date}', '{company_vacancy_id}')"
            )

        except Exception as _ex:
            logging.exception("ParserTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()