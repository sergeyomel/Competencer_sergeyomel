import logging

from src.db.requests.Writer import Writer

#Класс для работы с зарплатой
#Если зарплата в вакансии найдена, возвращает ее id
#Если такой зарплаты еще не было, то добавляет и возвращает id вставленной записи
class SalariesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):
        min = data['min']
        max = data['max']

        cursor = self.connection.cursor()

        try:
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
            return execute_result[0]

        except Exception as _ex:
            logging.exception("SalariesTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()