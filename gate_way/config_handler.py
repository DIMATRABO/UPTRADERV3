from configparser import ConfigParser
import json


class Config_handler :
    is_production:bool
    config_file:str
    parser:None
    data:None

    def __init__(self):
        self.parser=ConfigParser()
        self.config_file="./config/production.json"
        with open(self.config_file, "r") as jsonfile:
            self.data = json.load(jsonfile)
            self.is_production=self.data[0]['is_prod']
        if(self.is_production  == False):
            self.config_file="./config/testing.json"
            with open(self.config_file, "r") as jsonfile:
                self.data = json.load(jsonfile)
    

    def get_db_host(self):
        return self.data[1]['host']
    
    def get_db_port(self):
        return self.data[1]['port']

    def get_db_name(self):
        return self.data[1]['database']

    def get_db_user(self):
        return self.data[1]['user']
    
    def get_db_passwd(self):
        return self.data[1]['password']


 
    def get_log_file(self):
        return self.data[2]['log_file']

    def get_app_name(self):
        return self.data[3]["app_name"]