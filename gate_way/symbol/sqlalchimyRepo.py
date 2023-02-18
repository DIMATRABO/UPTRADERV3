

from gate_way.log import Log
from entities.entity import Base , SymbolEntity 
from model.model import Symbol
from sqlalchemy import exc , delete , or_
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self):
          self.Base = Base

        
    def save(self, session , symbol:Symbol):
        symbolEntity = SymbolEntity()
        symbolEntity.from_domain(model=symbol)
        if symbolEntity.symbol is None:
            raise Exception(e)

        session.add(symbolEntity)
        try:       
            session.commit()
        except exc.SQLAlchemyError as e:   
            logger.log(e)
            session.rollback()
            raise Exception(e)
         
        return symbolEntity.to_domain()
        

    
    def delete(self, session , symbol):
        if symbol.symbol is None:
            raise ValueError("symbol cannot be None")

        symbolEntity = SymbolEntity()
        symbolEntity.from_domain(model=symbol)
        #session.query(symbolEntity).filter(symbolEntity.symbol == symbol.symbol).delete()
        #symbolEntity = session.query(symbolEntity).filter(symbolEntity.symbol == symbol.symbol).one()
        #User.query.filter(User.id == 123).delete()
        print(symbolEntity)
        session.delete(symbolEntity)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception(e)

    def delete_list(self, session , symbol_list):
        symbol_entities = session.query(SymbolEntity).filter(or_(*(SymbolEntity.symbol == s for s in symbol_list))).all()
        for entity in symbol_entities:
            session.delete(entity)
        session.commit()

    def getAllSymbols(self, session):
        symbols = session.query(SymbolEntity).all()
        return [symbol.to_domain() for symbol in symbols]
        
    
    def getSymbolBySymbol(self, session , symbol):
        if symbol is None:
            raise ValueError("Symbol cannot be None")
        
        symbol_entity = session.query(SymbolEntity).filter(SymbolEntity.symbol == symbol).first()
        if symbol_entity is None:
            return None
        
        return symbol_entity.to_domain()


