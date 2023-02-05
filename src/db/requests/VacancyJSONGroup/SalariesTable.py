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
            if data['currency'] is None:
                return 1

            cursor.execute(
                """
                SELECT salary_id FROM salaries
                WHERE lower_threshold = %s
                AND upper_threshold = %s
                AND currency = %s
                AND gross = %s
                """,
                (data['min'], data['max'], data['currency'], data['gross'])
            )
            execute_result = cursor.fetchone()
            if execute_result is None:
                cursor.execute(
                    """
                    INSERT INTO salaries  (lower_threshold, upper_threshold, currency, gross)
                    VALUES (%s, %s, %s, %s)
                    RETURNING salary_id
                    """,
                    (data['min'], data['max'], data['currency'], data['gross'])
                )
                execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()