from psycopg2 import sql

from src.db.requests.Writer import Writer


class ResponsibilitiesTable(Writer):

    def __init__(self, connection, vacancy_id):
        Writer.__init__(self, connection)
        self.vacancy_id = vacancy_id

    def insert(self, data):
        responsibilities = set([item.strip() for item in data if len(item) < 1500 and len(item.strip()) > 2])
        if len(responsibilities) == 0:
            return

        cursor = self.connection.cursor()
        try:
            query = "insert into responsibilities (title) values {} on conflict (title) do update SET title = EXCLUDED.title  returning responsibility_id".format(
                ",".join("('" + item + "')" for item in responsibilities)
            )
            cursor.execute(query)
            insert_responsibility_data_set = [(resp_id[0], self.vacancy_id) for resp_id in cursor.fetchall()]
            if len(insert_responsibility_data_set) == 0:
                return

            query = sql.SQL('INSERT INTO vacancy_responsibilities (responsibility_id, vacancy_id) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, insert_responsibility_data_set))
            )
            cursor.execute(query)

        except Exception as _ex:
            raise

        finally:
            cursor.close()