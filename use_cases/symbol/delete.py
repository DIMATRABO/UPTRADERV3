from model.model import Symbol
from gate_way.dataBaseSession.sessionContext import SessionContext

class Delete:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, Symbol:Symbol):
        with self.sessionContext as session :
            result = self.repo.delete(session , Symbol)
            return result

