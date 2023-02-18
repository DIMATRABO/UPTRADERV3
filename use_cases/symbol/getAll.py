from use_cases.symbol.inputs.getAllInput import GetAllInput
from gate_way.dataBaseSession.sessionContext import SessionContext



class GetAll:
    def __init__(self , repo ):
        self.repo=repo
        self.sessionContext = SessionContext()


    def handle(self,getsymbolsInput:GetAllInput):
        with self.sessionContext as session : 
            if not getsymbolsInput.all is None :
                symbols = self.repo.getAllSymbols(session)
            if not getsymbolsInput.base is  None : 
                symbols = self.repo.getsymbolsByBase(session , getsymbolsInput.basee)
            return symbols

