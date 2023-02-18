from use_cases.config.inputs.getAllInput import GetAllInput
from gate_way.dataBaseSession.sessionContext import SessionContext



class GetAll:
    def __init__(self , repo ):
        self.repo=repo
        self.sessionContext = SessionContext()


    def handle(self,getconfigsInput:GetAllInput):
        with self.sessionContext as session : 
            if not getconfigsInput.all is None :
                configs = self.repo.getAllConfigs(session)
            if not getconfigsInput.base is  None : 
                configs = self.repo.getconfigsByConfig(session , getconfigsInput.basee)
            
            return configs

