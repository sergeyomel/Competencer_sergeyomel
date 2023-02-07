from src.db.config import resource_hh_db_id, resource_indeed_db_id, resource_linkedin_db_id

from src.db.requests.VacancyJSONGroup.CompanyVacanciesTable import CompanyVacanciesTable
from src.db.requests.Writer import Writer

#Класс для вставки значений в таблицу parsings на основе данных из json объекта
class ParserTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)
        self.company_vacancy_table = CompanyVacanciesTable(connection)

    def insert(self, data):
        company_vacancy_id = self.company_vacancy_table.insert(data)
        if data['parsing']['resource'] == "hh":
            resource_db_id = resource_hh_db_id
        elif data['parsing']['resource'] == "linkedin":
            resource_db_id = resource_linkedin_db_id
        else:
            resource_db_id = resource_indeed_db_id

        cursor = self.connection.cursor()
        try:
            query = """insert into parsings (resource_parsing_id, parsing_date, company_vacancy_id) 
                       values ('{}', '{}', '{}') on conflict (resource_parsing_id, parsing_date, company_vacancy_id) do update SET 
                       resource_parsing_id = EXCLUDED.resource_parsing_id,
                       parsing_date = EXCLUDED.parsing_date,
                       company_vacancy_id = EXCLUDED.company_vacancy_id
                    """.format(resource_db_id, data['parsing']['date'], company_vacancy_id
            )
            cursor.execute(query)

        except Exception as _ex:
            raise

        finally:
            cursor.close()
            