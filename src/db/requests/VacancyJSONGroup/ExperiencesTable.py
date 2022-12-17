
import logging

from src.db.requests.Writer import Writer

#Класс для работы с опытом работы
#Если опыт в вакансии найден, возвращает его id
#Если такого опыта еще не было, то добавляет и возвращает id вставленной записи

class ExperiencesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):
        exp = data

        cursor = self.connection.cursor()

        try:
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
            return execute_result[0]

        except Exception as _ex:
            logging.exception("ExperiencesTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()