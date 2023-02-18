from gate_way.dataBaseSession.sessionContext import SessionContext

class GetAll:
    def __init__(self , repo ):
        self.repo=repo
        self.sessionContext = SessionContext()


    def handle(self,symbol):
        with self.sessionContext as session : 
                actions = self.repo.getActionsBySymbol(session , symbol)
                return actions

