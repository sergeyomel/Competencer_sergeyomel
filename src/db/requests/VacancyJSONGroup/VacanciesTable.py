from src.db.requests.Writer import Writer

class VacanciesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):

        cursor = self.connection.cursor()
        try:
            query = """INSERT INTO vacancies (title, platform_id)
                       VALUES ('{}', '{}')
                       RETURNING vacancy_id
                    """.format(data['title'], data['id'])
            cursor.execute(query)
            execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()