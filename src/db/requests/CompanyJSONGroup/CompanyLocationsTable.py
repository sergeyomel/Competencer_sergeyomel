import psycopg2

from src.db.requests.CompanyJSONGroup.CompaniesTable import CompaniesTable
from src.db.requests.CompanyJSONGroup.LocationsTable import LocationsTable
from src.db.requests.Writer import Writer

class CompanyLocationsTable(Writer):

    def __init__(self, host, user, password, db_name):
        Writer.__init__(self, host, user, password, db_name)

        self.companies_table = CompaniesTable(host, user, password, db_name)
        self.locations_table = LocationsTable(host, user, password, db_name)

    def insert(self, data):
        company_location = data['location']

        company_id = self.companies_table.insert(data)
        company_location_id = self.locations_table.insert(company_location)

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
                    f" INSERT INTO company_locations (company_id, location_id) "
                    f" VALUES ('{company_id}', '{company_location_id}')"
                )
                print("[INFO] Data in CompanyLocationsTable was successfully inserted")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL in CompanyLocationsTable ", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")