

from gate_way.log import Log
from entities.entity import Base , ActionEntity 
from model.model import Action
from sqlalchemy import exc  , or_
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self):
          self.Base = Base

        
    def save(self, session , action:Action):
        actionEntity = ActionEntity()
        actionEntity.from_domain(model=action)
        if actionEntity.id is None:
            actionEntity.id = str(uuid.uuid4())

        session.add(actionEntity)
        try:       
            session.commit()
        except exc.SQLAlchemyError as e:   
            logger.log(e)
            session.rollback()
            raise Exception(e)
         
        return actionEntity.to_domain()
        

    
    def delete(self, session , action):
        if action.action is None:
            raise ValueError("action cannot be None")

        actionEntity = ActionEntity()
        actionEntity.from_domain(model=action)
        print(actionEntity)
        session.delete(actionEntity)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception(e)


    def getAllActions(self, session):
        actions = session.query(ActionEntity).all()
        return [action.to_domain() for action in actions]
        
    
    def getActionsBySymbol(self, session , symbol):
        if symbol is None:
            raise ValueError("symbol cannot be None")
        actions_entity = session.query(ActionEntity).filter(ActionEntity.symbol == symbol).order_by(ActionEntity.timestamp.desc()).all()
        return [action.to_domain() for action in actions_entity]
        