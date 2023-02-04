from src.db.requests.CompanyJSONGroup.CompaniesTable import CompaniesTable
from src.db.requests.CompanyJSONGroup.LocationsTable import LocationsTable
from src.db.requests.Writer import Writer

class CompanyLocationsTable(Writer):

    def __init__(self, connection):
        Writer.__init__(self, connection)

        self.companies_table = CompaniesTable(connection)
        self.locations_table = LocationsTable(connection)

    def insert(self, data):
        company_location = data['location']

        company_id = self.companies_table.insert(data)
        company_location_id = self.locations_table.insert(company_location)

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                f" INSERT INTO company_locations (company_id, location_id) "
                f" VALUES ('{company_id}', '{company_location_id}')"
            )

        except Exception as _ex:
            raise

        finally:
            cursor.close()