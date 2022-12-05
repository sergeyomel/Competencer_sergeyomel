import json

from config import host, user, password, db_name
from src.db.requests.DbLoader import DbLoader
from src.db.mocks import mocks

if __name__ == "__main__":
    loader = DbLoader(host, user, password, db_name)

    loader.load(mocks.data)