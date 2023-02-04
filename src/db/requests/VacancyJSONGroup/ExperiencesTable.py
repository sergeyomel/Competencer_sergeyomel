
import logging

from src.db.requests.Writer import Writer

#Класс для работы с опытом работы
#Если опыт в вакансии найден, возвращает его id
#Если такого опыта еще не было, то добавляет и возвращает id вставленной записи

class ExperiencesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):
        exp_min = data["min"]
        exp_max = data["max"]

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                f" SELECT experience_id FROM experiences "
                f" WHERE exp_min = '{exp_min}' AND exp_max = '{exp_max}'"
            )
            execute_result = cursor.fetchone()
            if execute_result is None:
                cursor.execute(
                    f" INSERT INTO experiences (exp_min, exp_max) "
                    f" VALUES  ('{exp_min}', '{exp_max}') "
                    f" RETURNING experience_id"
                    )
                execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()