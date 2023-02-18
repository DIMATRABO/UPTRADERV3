from model.model import Symbol
from gate_way.dataBaseSession.sessionContext import SessionContext

class Delete:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, symbol_list):
        with self.sessionContext as session :
            result = self.repo.delete_list(session , symbol_list)
            return result

