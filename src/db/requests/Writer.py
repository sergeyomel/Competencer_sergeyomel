#Родительский класс для вставки данных в таблицы

class Writer:

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def insert(self, data):
        pass