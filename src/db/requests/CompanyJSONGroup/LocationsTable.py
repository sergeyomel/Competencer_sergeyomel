import psycopg2

from src.db.requests.Writer import Writer


class LocationsTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

    def insert(self, data):
        country = data['country']
        city = data['city']
        street = data['street']

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
                    f"SELECT location_id FROM locations WHERE country = '{country}' AND city = '{city}' AND street = '{street}'"
                )
                execute_result = cursor.fetchone()
                if execute_result is None:
                    cursor.execute(
                        f" INSERT INTO locations (country, city, street) "
                        f" VALUES ('{country}', '{city}', '{street}') "
                        f" RETURNING location_id"
                    )
                    execute_result = cursor.fetchone()

                print("[INFO] Data in LocationsTable was successfully inserted")
                return execute_result[0]

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in LocationsTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")