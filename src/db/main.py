from src.db.mocks import mocks
from src.db.requests.DbLoader import DbLoader

if __name__ == "__main__":
    loader = DbLoader()
    loader.load(mocks.data)