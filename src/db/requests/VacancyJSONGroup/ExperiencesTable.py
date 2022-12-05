import json

import psycopg2

from src.db.requests.Writer import Writer

#Класс для работы с опытом работы
#Если опыт в вакансии найден, возвращает его id
#Если такого опыта еще не было, то добавляет и возвращает id вставленной записи

class ExperiencesTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

    def insert(self, data):
        exp = data

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
                    f" SELECT experience_id FROM experiences "
                    f" WHERE experience = {exp} "
                )
                execute_result = cursor.fetchone()
                if execute_result is None:
                    cursor.execute(
                        f" INSERT INTO experiences (experience) "
                        f" VALUES  ({exp}) "
                        f" RETURNING experience_id"
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