import json

import psycopg2

from src.db.requests.Writer import Writer


class VacanciesTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

    def insert(self, title):

        #Добавить заполнение развязочных таблиц

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
                    f" INSERT INTO vacancies (title) "
                    f" VALUES ('{title}')"
                    f" RETURNING vacancy_id"
                )
                execute_result = cursor.fetchone()
                print("[INFO] Data was successfully inserted")
                return execute_result[0]

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")