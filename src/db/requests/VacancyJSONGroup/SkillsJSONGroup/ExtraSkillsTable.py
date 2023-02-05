import logging

import psycopg2
from psycopg2 import sql

from src.db.requests.Writer import Writer


class ExtraSkillsTable(Writer):

    def __init__(self, connection, vacancy_id):
        Writer.__init__(self, connection)
        self.vacancy_id = vacancy_id

    def insert(self, data):
        extra_skills = [item for item in data if len(item) < 1500]

        if len(extra_skills) == 0:
            return

        skills_id = []

        cursor = self.connection.cursor()

        try:
            for skill in extra_skills:
                skill = skill.strip()
                if not skill or len(skill) < 2:
                    continue
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
            if len(skills_id) == 0:
                return

            insert_extra_skills_data = []
            for skill_id in skills_id:
                insert_extra_skills_data.append((skill_id, self.vacancy_id))

            insert_extra_skills_data_set = set(insert_extra_skills_data)

            insert = sql.SQL('INSERT INTO extra_skills (skill_id, vacancy_id) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, insert_extra_skills_data_set))
            )
            cursor.execute(insert)

        except Exception as _ex:
            raise

        finally:
            cursor.close()