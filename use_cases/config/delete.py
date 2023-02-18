from model.model import Config
from gate_way.dataBaseSession.sessionContext import SessionContext

class Delete:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, Config:Config):
        with self.sessionContext as session :
            result = self.repo.delete(session , Config)
            return result

