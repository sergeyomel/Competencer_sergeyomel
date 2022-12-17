import logging

import psycopg2
from psycopg2 import sql

from src.db.requests.Writer import Writer


class ResponsibilitiesTable(Writer):

    def __init__(self, connection, vacancy_id):
        Writer.__init__(self, connection)
        self.vacancy_id = vacancy_id

    def insert(self, data):
        responsibilities = data['responsibilities']

        if len(responsibilities) == 0:
            return

        responsibility_id = []

        cursor = self.connection.cursor()

        try:
            for responsibility in responsibilities:
                cursor.execute(
                    f" SELECT responsibility_id FROM responsibilities "
                    f" WHERE title = '{responsibility}'"
                )
                execute_result = cursor.fetchone()
                if execute_result is None:
                    cursor.execute(
                        f" INSERT INTO responsibilities (title)"
                        f" VALUES ('{responsibility}') "
                        f" RETURNING responsibility_id "
                    )
                    execute_result = cursor.fetchone()
                responsibility_id.append(execute_result[0])

            insert_responsibility_data = []
            for responsibility_id in responsibility_id:
                insert_responsibility_data.append((responsibility_id, self.vacancy_id))

            insert = sql.SQL('INSERT INTO vacancy_responsibilities (responsibility_id, vacancy_id) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, insert_responsibility_data))
            )
            cursor.execute(insert)

        except Exception as _ex:
            logging.exception("ResponsibilitiesTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()