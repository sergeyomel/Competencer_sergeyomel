import psycopg2
from psycopg2 import sql

from src.db.requests.Writer import Writer


class NecessarySkillsTable(Writer):

    def __init__(self, host, user, password, db_name, vacancy_id):
        Writer.__init__(self, host, user, password, db_name)
        self.vacancy_id = vacancy_id

    def insert(self, data):
        necessary_skills = data['necessary']

        if len(necessary_skills) == 0:
            return

        skills_id = []

        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                database=self.db_name,
                password=self.password
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
                for skill in necessary_skills:
                    cursor.execute(
                        f" SELECT skill_id FROM skills "
                        f" WHERE title = '{skill}'"
                    )
                    execute_result = cursor.fetchone()
                    if execute_result is None:
                        cursor.execute(
                            f" INSERT INTO skills (title)"
                            f" VALUES ('{skill}') "
                            f" RETURNING skill_id "
                        )
                        execute_result = cursor.fetchone()
                    skills_id.append(execute_result[0])

                insert_necessary_skill_data = []
                for skill_id in skills_id:
                    insert_necessary_skill_data.append((skill_id, self.vacancy_id))

                insert = sql.SQL('INSERT INTO necessary_skills (skill_id, vacancy_id) VALUES {}').format(
                    sql.SQL(',').join(map(sql.Literal, insert_necessary_skill_data))
                )
                cursor.execute(insert)

                print("[INFO] Data in NecessarySkillsTable was successfully inserted")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in NecessarySkillsTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")