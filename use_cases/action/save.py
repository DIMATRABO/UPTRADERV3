from model.model import Action
from gate_way.dataBaseSession.sessionContext import SessionContext

class Save:
    def __init__(self, repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, action:Action):
        with self.sessionContext as session : 
            return self.repo.save(session , action)
         
