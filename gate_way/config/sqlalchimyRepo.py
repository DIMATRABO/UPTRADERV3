

from gate_way.log import Log
from entities.entity import Base , ConfigEntity 
from model.model import Config
from sqlalchemy import exc , delete , or_


logger = Log()
class SqlAlchimy_repo :
    def __init__(self):
          self.Base = Base

        
    def save(self, session , config:Config):
        configEntity = ConfigEntity()
        configEntity.from_domain(model=config)
        if configEntity.symbol is None:
            raise Exception(e)

        session.merge(configEntity)
        try:       
            session.commit()
        except exc.SQLAlchemyError as e:   
            logger.log(e)
            session.rollback()
            raise Exception(e)
         
        return configEntity.to_domain()
        

    
    def delete(self, session , config):
        if config.config is None:
            raise ValueError("config cannot be None")

        configEntity = ConfigEntity()
        configEntity.from_domain(model=config)
        #session.query(configEntity).filter(configEntity.config == config.config).delete()
        #configEntity = session.query(configEntity).filter(configEntity.config == config.config).one()
        #User.query.filter(User.id == 123).delete()
        print(configEntity)
        session.delete(configEntity)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception(e)

    def delete_list(self, session , config_list):
        config_entities = session.query(ConfigEntity).filter(or_(*(ConfigEntity.config == s for s in config_list))).all()
        for entity in config_entities:
            session.delete(entity)
        session.commit()

    def getAllConfigs(self, session):
        Configs = session.query(ConfigEntity).all()
        return [Config.to_domain() for Config in Configs]
        
    
    def getConfigByConfig(self, session , config):
        if config is None:
            raise ValueError("Config cannot be None")
        
        config_entity = session.query(ConfigEntity).filter(ConfigEntity.config == config).first()
        if config_entity is None:
            return None
        
        return config_entity.to_domain()


