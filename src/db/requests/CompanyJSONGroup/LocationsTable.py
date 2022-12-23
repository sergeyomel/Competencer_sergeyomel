import logging

import psycopg2

from src.db.requests.Writer import Writer


class LocationsTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):
        country = data['country']
        city = data['city']
        street = data['street']

        cursor = self.connection.cursor()

        try:
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

            return execute_result[0]

        except Exception as _ex:
            logging.exception("LocationsTable", exc_info=True)
            self.connection.close()

        finally:
            cursor.close()