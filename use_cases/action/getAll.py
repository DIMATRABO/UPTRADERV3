from gate_way.dataBaseSession.sessionContext import SessionContext



class GetAll:
    def __init__(self , repo ):
        self.repo=repo
        self.sessionContext = SessionContext()


    def handle(self):
        with self.sessionContext as session : 
            actions = self.repo.getAllActions(session)
            return actions

