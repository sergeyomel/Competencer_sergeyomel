import json
import logging
import psycopg2
from datetime import datetime

from src.db.requests.CompanyJSONGroup.CompanyLocationsTable import CompanyLocationsTable
from src.db.requests.ParsingsJSONGroup.ParserTable import ParserTable
from src.db.config import host, user, password, db_name


# Класс для загрузки json объектов в БД.
# Принимает на вход список из JSON объектов, описывающих вакансию
class DbLoader:

    def __init__(self):
        logging.basicConfig(filename="DataBaseExceptionLog.log", filemode="a", level=logging.INFO, encoding='utf-8')

    def load(self, json_data):

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                database=db_name,
                password=password
            )
            connection.autocommit = True
            cursor = connection.cursor()

            company_locations = CompanyLocationsTable(connection)
            parsers_table = ParserTable(connection)

            json_data = json.loads(json.dumps(json_data).replace("'", ""))

            for item in json_data:
                try:
                    platform_id = item['vacancy']['id']

                    cursor.execute(
                        f" SELECT COUNT(platform_id) "
                        f" FROM vacancies"
                        f" WHERE platform_id = '{platform_id}' "
                    )
                    execute_result = cursor.fetchone()
                    if(execute_result[0] == 0):
                        company_locations.insert(item['company'])
                        parsers_table.insert(item)

                except Exception as _ex:
                    logging.info("  Date: {}".format(datetime.now()))
                    logging.exception("DbLoader",  exc_info=True)
                    logging.info(item)
                    logging.info("------------------------------------------------------------------------------------")

            connection.close()

            logging.info("Data insert was successful.")

        except Exception as _ex:
            logging.exception("DbLoader", exc_info=True)

