from src.db.requests.Writer import Writer

class VacanciesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):

        title = data['title']
        platform_id = data['id']

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                f" INSERT INTO vacancies (title, platform_id) "
                f" VALUES ('{title}', '{platform_id}')"
                f" RETURNING vacancy_id"
            )
            execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()