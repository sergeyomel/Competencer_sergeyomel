import logging

from src.db.requests.Writer import Writer

#Класс для работы с зарплатой
#Если зарплата в вакансии найдена, возвращает ее id
#Если такой зарплаты еще не было, то добавляет и возвращает id вставленной записи
class SalariesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):

        cursor = self.connection.cursor()

        try:
            query = "SELECT salary_id FROM salaries WHERE lower_threshold = {} AND upper_threshold = {} AND currency {} AND gross {}".format(
                "'" + str(data['min']) + "'",
                "'" + str(data['max']) + "'",
                "is null" if data['currency'] is None else "= '{}'".format(data['currency']),
                "is null" if data['gross'] is None else "= {}".format(data['gross']))
            cursor.execute(query)
            execute_result = cursor.fetchone()
            if execute_result is None:
                query = "INSERT INTO salaries  (lower_threshold, upper_threshold, currency, gross) VALUES ({}, {}, {}, {}) RETURNING salary_id".format(
                    "'" + str(data['min']) + "'",
                    "'" + str(data['max']) + "'",
                    "NULL" if data['currency'] is None else "'{}'".format(data['currency']),
                    "NULL" if data['gross'] is None else "'{}'".format(data['gross']))
                cursor.execute(query)
                execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()