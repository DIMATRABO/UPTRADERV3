from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities.entity import Base

class Db_creator :
    def __init__(self, config):
        self.dbname = config.get_db_name()
        self.user = config.get_db_user()
        self.password = config.get_db_passwd()
        self.port = config.get_db_port()
        self.host=config.get_db_host()

        self.engine = create_engine("postgresql+psycopg2://"+self.user+":"+self.password+"@"+self.host+":"+str(self.port)+"/"+self.dbname)
        self.Base = Base

    def create(self):
        self.Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        session=Session()
        session.commit()