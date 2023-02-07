import json
import logging
import psycopg2
from datetime import datetime
from psycopg2 import sql
import time

from src.db.requests.CompanyJSONGroup.CompanyLocationsTable import CompanyLocationsTable
from src.db.requests.ParsingsJSONGroup.ParserTable import ParserTable
from src.db.config import host, user, password, db_name


# Класс для загрузки json объектов в БД.
# Принимает на вход список из JSON объектов, описывающих вакансию
class DbLoader:

    def __init__(self):
        logging.basicConfig(filename="DataBaseExceptionLog.log", filemode="a", level=logging.INFO, encoding='utf-8')

    def load(self, json_data):

        connection = psycopg2.connect(
            host=host,
            user=user,
            database=db_name,
            password=password
        )
        count_rollback = 0
        count_insert_data = 0

        connection.autocommit = False
        cursor = connection.cursor()

        receiced_platform_id = set([item['vacancy']['id'] for item in json_data])
        if len(receiced_platform_id) == 0:
            return

        try:
            company_locations = CompanyLocationsTable(connection)
            parsers_table = ParserTable(connection)

            json_data = json.loads(json.dumps(json_data).replace("'", ""))

            insert = sql.SQL('SELECT platform_id FROM vacancies WHERE platform_id IN ({})').format(
                sql.SQL(',').join(map(sql.Literal, receiced_platform_id))
            )
            cursor.execute(insert)
            contain_db_platform_id = set([id[0] for id in cursor.fetchall()])
            ids_not_in_db = list(receiced_platform_id.difference(contain_db_platform_id))

            start = time.time()
            for item in json_data:
                if item['vacancy']['id'] in ids_not_in_db:
                    try:
                        company_locations.insert(item['company'])
                        parsers_table.insert(item)

                        count_insert_data += 1
                        connection.commit()

                    except Exception as _ex:
                        connection.rollback()

                        logging.info("  Date: {}. Connection rollback.".format(datetime.now()))
                        logging.exception("DbLoader: load json_item",  exc_info=True)
                        logging.info(item)
                        logging.info("--------------------------------------------------------------------------------")

            connection.close()

            end = time.time() - start
            logging.info(f"Data insert was successful. Time: {end}, Count insert JSON item: {count_insert_data}, Count rollback: {count_rollback}")

        except Exception as _ex:
            count_rollback += 1
            logging.info(" Date: {}".format(datetime.now()))
            logging.exception("DbLoader", exc_info=True)
            logging.info(" JSON data:")
            logging.info(json_data)
            logging.info("------------------------------------------------------------------------------------")

        finally:
            if connection:
                cursor.close()
                connection.close()

