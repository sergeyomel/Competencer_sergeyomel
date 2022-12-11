import psycopg2

from src.db.requests.Writer import Writer


class CompaniesTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

    def insert(self, data):
        name = data['name']

        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                database=self.db_name,
                password=self.password
            )
            connection.autocommit = True

            with connection.cursor() as cursor:
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
                print("[INFO] Data in CompaniesTable was successfully inserted")
                return execute_command[0]

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in CompaniesTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")


