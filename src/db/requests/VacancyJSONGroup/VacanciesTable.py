import logging

from src.db.requests.Writer import Writer


class VacanciesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

        logging.basicConfig(level=logging.INFO, filename="dataload.log", filemode="w")

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
            logging.exception("VacanciesTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()