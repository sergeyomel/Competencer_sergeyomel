from src.db.requests.Writer import Writer

class CompaniesTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):

        cursor = self.connection.cursor()
        try:
            query = f"insert into companies (company_name) values ('{data['name']}') on conflict (company_name) do update SET company_name = EXCLUDED.company_name returning company_id"
            cursor.execute(query)
            execute_command = cursor.fetchone()
            return execute_command[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()


