#Родительский класс для вставки данных в таблицы

class Writer:

    def __init__(self, connection):
        self.connection = connection

    def insert(self, data):
        pass