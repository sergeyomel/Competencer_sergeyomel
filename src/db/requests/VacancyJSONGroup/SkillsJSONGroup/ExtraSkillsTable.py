from psycopg2 import sql

from src.db.requests.Writer import Writer


class ExtraSkillsTable(Writer):

    def __init__(self, connection, vacancy_id):
        Writer.__init__(self, connection)
        self.vacancy_id = vacancy_id

    def insert(self, data):
        extra_skills = set([item for item in data if len(item) < 1500 and len(item.strip()) > 2])
        if len(extra_skills) == 0:
            return

        cursor = self.connection.cursor()
        try:
            query = "insert into skills (title) values {} on conflict (title) do update SET title = EXCLUDED.title  returning skill_id".format(
                ",".join("('" + item + "')" for item in extra_skills)
            )
            cursor.execute(query)
            insert_extra_skills_data_set = [(skill_id[0], self.vacancy_id) for skill_id in cursor.fetchall()]
            if len(insert_extra_skills_data_set) == 0:
                return

            query = sql.SQL('INSERT INTO extra_skills (skill_id, vacancy_id) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, insert_extra_skills_data_set))
            )
            cursor.execute(query)

        except Exception as _ex:
            raise

        finally:
            cursor.close()