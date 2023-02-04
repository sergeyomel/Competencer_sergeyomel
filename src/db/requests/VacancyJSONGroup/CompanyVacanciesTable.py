import json
import logging

import psycopg2

from src.db.requests.CompanyJSONGroup.CompaniesTable import CompaniesTable
from src.db.requests.VacancyJSONGroup.ResponsibilitiesJSONGroup.ResponsibilitiesTable import ResponsibilitiesTable
from src.db.requests.VacancyJSONGroup.SalariesTable import SalariesTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.SkillsLoader import SkillsLoader
from src.db.requests.VacancyJSONGroup.VacanciesTable import VacanciesTable
from src.db.requests.VacancyJSONGroup.ExperiencesTable import ExperiencesTable
from src.db.requests.Writer import Writer


class CompanyVacanciesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

        self.companies_table = CompaniesTable(connection)
        self.vacancies_table = VacanciesTable(connection)
        self.experience_table = ExperiencesTable(connection)
        self.salaries_table = SalariesTable(connection)

    def insert(self, data):
        company_id = self.companies_table.insert(data['company'])

        data = data['vacancy']

        publication_date = data['publicDate']
        description = data['description']
        if len(description) > 1000:
            description = ''

        vacancy_id = self.vacancies_table.insert({"title": data['title'], "id": data['id']})
        experience_id = self.experience_table.insert(data['workExp'])
        salary_id = self.salaries_table.insert(data['salary'])

        skills_loader = SkillsLoader(self.connection, vacancy_id)
        responsibility_table = ResponsibilitiesTable(self.connection, vacancy_id)
        skills_loader.insert(data['skills'])
        responsibility_table.insert(data)

        cursor = self.connection.cursor()

        try:
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
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()