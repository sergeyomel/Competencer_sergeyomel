from src.db.requests.Writer import Writer

class CompaniesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):
        name = data['name']

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                f"SELECT company_id FROM companies WHERE company_name = '{name}'"
            )
            execute_command = cursor.fetchone()
            if execute_command is None:
                cursor.execute(
                    f"INSERT INTO companies (company_name) "
                    f" VALUES ('{name}') "
                    f" RETURNING company_id"
                )
                execute_command = cursor.fetchone()
            return execute_command[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()


