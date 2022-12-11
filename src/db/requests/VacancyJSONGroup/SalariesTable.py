import json

import psycopg2

from src.db.requests.Writer import Writer

#Класс для работы с зарплатой
#Если зарплата в вакансии найдена, возвращает ее id
#Если такой зарплаты еще не было, то добавляет и возвращает id вставленной записи
class SalariesTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

    def insert(self, data):
        min = data['min']
        max = data['max']

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
                    f" SELECT salary_id FROM salaries "
                    f" WHERE lower_threshold = {min} "
                    f" AND upper_threshold = {max} "
                )
                execute_result = cursor.fetchone()
                if execute_result is None:
                    cursor.execute(
                        f" INSERT INTO salaries (lower_threshold, upper_threshold) "
                        f" VALUES ({min}, {max}) "
                        f" RETURNING salary_id"
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