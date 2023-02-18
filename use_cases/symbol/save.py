from model.model import Symbol
from gate_way.dataBaseSession.sessionContext import SessionContext

class Save:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, symbol:Symbol):
        with self.sessionContext as session : 
            return self.repo.save(session , symbol)
         
