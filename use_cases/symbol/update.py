from models.model import Template
from gate_ways.dataBaseSession.sessionContext import SessionContext

class Update:
    def __init__(self ,repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, template:Template):
        with self.sessionContext as session : 
            return  self.repo.update(session , template)
       