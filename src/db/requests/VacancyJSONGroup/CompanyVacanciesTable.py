import json
import psycopg2

from src.db.requests.CompanyJSONGroup.CompaniesTable import CompaniesTable
from src.db.requests.VacancyJSONGroup.ResponsibilitiesJSONGroup.ResponsibilitiesTable import ResponsibilitiesTable
from src.db.requests.VacancyJSONGroup.SalariesTable import SalariesTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.SkillsLoader import SkillsLoader
from src.db.requests.VacancyJSONGroup.VacanciesTable import VacanciesTable
from src.db.requests.VacancyJSONGroup.ExperiencesTable import ExperiencesTable
from src.db.requests.Writer import Writer


class CompanyVacanciesTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

        self.companies_table = CompaniesTable(host, user, password, db_name)
        self.vacancies_table = VacanciesTable(host, user, password, db_name)
        self.experience_table = ExperiencesTable(host, user, password, db_name)
        self.salaries_table = SalariesTable(host, user, password, db_name)

    def insert(self, data):
        company_id = self.companies_table.insert(data['company'])

        data = data['vacancy']

        publication_date = data['publicDate']
        description = data['description']

        vacancy_id = self.vacancies_table.insert(data['title'])
        experience_id = self.experience_table.insert(data['workExp'])
        salary_id = self.salaries_table.insert(data['salary'])

        skills_loader = SkillsLoader(self.host, self.user, self.password, self.db_name, vacancy_id)
        responsibility_table = ResponsibilitiesTable(self.host, self.user, self.password, self.db_name, vacancy_id)
        skills_loader.insert(data['skills'])
        responsibility_table.insert(data)

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
                    f" INSERT INTO company_vacancies "
                    f" (publication_date, description, company_id, experience_id, salary_id, vacancy_id) "
                    f" VALUES "
                    f" ('{publication_date}', "
                    f"  '{description}', "
                    f"   {company_id}, "
                    f"   {experience_id}, "
                    f"   {salary_id}, "
                    f"   {vacancy_id}) "
                    f" RETURNING company_vacancy_id "
                )
                execute_result = cursor.fetchone()
                print("[INFO] Data in CompanyVacanciesTable was successfully inserted")
                return execute_result[0]

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in CompanyVacanciesTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")