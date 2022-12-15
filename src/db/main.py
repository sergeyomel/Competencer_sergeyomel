
from src.db.requests.DbLoader import DbLoader
from src.db.mocks import mocks

if __name__ == "__main__":
    loader = DbLoader()

    loader.load(mocks.data)