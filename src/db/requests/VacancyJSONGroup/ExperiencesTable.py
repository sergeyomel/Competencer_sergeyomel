
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
            query = """insert into experiences (exp_min, exp_max) 
                        values ('{}', '{}') on conflict (exp_min, exp_max) do update SET 
                        exp_min = EXCLUDED.exp_min,
                        exp_max = EXCLUDED.exp_max
                        returning experience_id""".format(
                        data['min'], data['max']
                        )

            cursor.execute(query)
            execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()