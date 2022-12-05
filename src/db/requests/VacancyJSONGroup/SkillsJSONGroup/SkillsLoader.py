from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.ExtraSkillsTable import ExtraSkillsTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.KeySkillsTable import KeySkillsTable
from src.db.requests.VacancyJSONGroup.SkillsJSONGroup.NecessarySkillsTable import NecessarySkillsTable
from src.db.requests.Writer import Writer


class SkillsLoader(Writer):

    def __init__(self, host, user, password, db_name, vacancy_id):
        Writer.__init__(self, host, user, password, db_name)

        self.necessary_skill_table = NecessarySkillsTable(host, user, password, db_name, vacancy_id)
        self.extra_skill_table = ExtraSkillsTable(host, user, password, db_name, vacancy_id)
        self.key_skill_table = KeySkillsTable(host, user, password, db_name, vacancy_id)

    def insert(self, data):
        self.necessary_skill_table.insert(data)
        self.extra_skill_table.insert(data)
        self.key_skill_table.insert(data)