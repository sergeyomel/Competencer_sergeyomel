from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.ExtraSkillsTable import ExtraSkillsTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.KeySkillsTable import KeySkillsTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.NecessarySkillsTable import NecessarySkillsTable
from src.db.requests.Writer import Writer


class SkillsLoader(Writer):

    def __init__(self, connection, vacancy_id):
        Writer.__init__(self, connection)

        self.necessary_skill_table = NecessarySkillsTable(connection, vacancy_id)
        self.extra_skill_table = ExtraSkillsTable(connection, vacancy_id)
        self.key_skill_table = KeySkillsTable(connection, vacancy_id)

    def insert(self, data):
        self.necessary_skill_table.insert(data['necessary'])
        self.extra_skill_table.insert(data['extra'])
        self.key_skill_table.insert(data['key'])