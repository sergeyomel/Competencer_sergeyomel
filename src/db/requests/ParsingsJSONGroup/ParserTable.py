import psycopg2

from src.db.requests.VacancyJSONGroup.CompanyVacanciesTable import CompanyVacanciesTable
from src.db.requests.Writer import Writer

#Класс для вставки значений в таблицу parsings на основе данных из json объекта
class ParserTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)
        self.company_vacancy_table = CompanyVacanciesTable(host, user, password, db_name)

    def insert(self, data):
        parsing_date = data['parsing']['date']
        resource_title = data['parsing']['resource']

        company_vacancy_id = self.company_vacancy_table.insert(data)

        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                database=self.db_name,
                password=self.password
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT resource_id FROM resources WHERE title = '{resource_title}'"
                )
                resource_id = cursor.fetchone()[0]
                cursor.execute(
                    f" INSERT INTO parsings (resource_parsing_id, parsing_date, company_vacancy_id) "
                    f" VALUES ('{resource_id}', '{parsing_date}', '{company_vacancy_id}')"
                )
                print("[INFO] Data in ParserTable was successfully inserted")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in ParserTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")