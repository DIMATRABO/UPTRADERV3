from gate_way.dataBaseSession.sessionContext import SessionContext

class GetOne:
    def __init__(self ,  repo):
        self.repo=repo
        self.sessionContext = SessionContext()

    def handel(self, symbol):
        with self.sessionContext as session :
            symbol = self.repo.getSymbolBySymbol(session , symbol)
            return symbol
