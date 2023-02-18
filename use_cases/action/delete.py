from model.model import Action
from gate_way.dataBaseSession.sessionContext import SessionContext

class Delete:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, action:Action):
        with self.sessionContext as session :
            result = self.repo.delete(session , action)
            return result

