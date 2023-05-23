from src.db.requests.Writer import Writer


class LocationsTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

    def insert(self, data):

        cursor = self.connection.cursor()
        try:
            query = """insert into locations (country, city, street) 
                       values ('{}', '{}', '{}') on conflict (country, city, street) do update SET 
                       country = EXCLUDED.country,
                       city = EXCLUDED.city,
                       street = EXCLUDED.street
                       returning location_id""".format(
                    data['country'], data['city'], data['street']
            )
            cursor.execute(query)
            execute_result = cursor.fetchone()
            return execute_result[0]

        except Exception as _ex:
            raise

        finally:
            cursor.close()