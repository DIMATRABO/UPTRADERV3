from sqlalchemy import Column, String , DateTime, Float , Boolean, Integer
from sqlalchemy.orm import declarative_base
from model.model import *

Base = declarative_base()

class SymbolEntity(Base):
    __tablename__ = "symbols"
    baseCurrency = Column("baseCurrency",String)
    baseIncrement = Column("baseIncrement",String)
    baseMaxSize = Column("baseMaxSize",String)
    baseMinSize = Column("baseMinSize",String)
    enableTrading = Column("enableTrading",Boolean)
    feeCurrency = Column("feeCurrency",String)
    isMarginEnabled = Column("isMarginEnabled",Boolean)
    market = Column("market",String)
    minFunds = Column("minFunds",String)
    name = Column("name",String)
    priceIncrement = Column("priceIncrement",String)
    priceLimitRate = Column("priceLimitRate",String)
    quoteCurrency = Column("quoteCurrency",String)
    quoteIncrement = Column("quoteIncrement",String)
    quoteMaxSize = Column("quoteMaxSize",String)
    quoteMinSize = Column("quoteMinSize",String)
    symbol = Column("symbol",String , primary_key=True)

    def __init__(self , baseCurrency=None , baseIncrement=None , baseMaxSize =None , baseMinSize=None , enableTrading=None , feeCurrency=None ,isMarginEnabled=None ,market=None ,minFunds=None ,name=None ,priceIncrement=None ,priceLimitRate=None , quoteCurrency=None ,quoteIncrement=None , quoteMaxSize=None , quoteMinSize=None ,symbol=None):
        self.baseCurrency = baseCurrency
        self.baseIncrement = baseIncrement
        self.baseMaxSize = baseMaxSize
        self.baseMinSize = baseMinSize
        self.enableTrading = enableTrading
        self.feeCurrency = feeCurrency
        self.isMarginEnabled = isMarginEnabled
        self.market = market
        self.minFunds = minFunds
        self.name = name
        self.priceIncrement = priceIncrement
        self.priceLimitRate = priceLimitRate
        self.quoteCurrency = quoteCurrency
        self.quoteIncrement = quoteIncrement
        self.quoteMaxSize = quoteMaxSize
        self.quoteMinSize = quoteMinSize
        self.symbol = symbol

    def __repr__(self):
        return "<Symbol (symbol='%s')>" % (
            self.symbol
        )
    
    def from_domain(self,model : Symbol):
            self.baseCurrency= model.baseCurrency
            self.baseIncrement= model.baseIncrement
            self.baseMaxSize= model.baseMaxSize
            self.baseMinSize= model.baseMinSize
            self.enableTrading= model.enableTrading
            self.feeCurrency= model.feeCurrency
            self.isMarginEnabled= model.isMarginEnabled
            self.market= model.market
            self.minFunds= model.minFunds
            self.name= model.name
            self.priceIncrement= model.priceIncrement
            self.priceLimitRate= model.priceLimitRate
            self.quoteCurrency= model.quoteCurrency
            self.quoteIncrement= model.quoteIncrement
            self.quoteMaxSize= model.quoteMaxSize
            self.quoteMinSize= model.quoteMinSize
            self.symbol= model.symbol

    def to_domain(self):
        return Symbol(
            self.baseCurrency,
            self.baseIncrement,
            self.baseMaxSize,
            self.baseMinSize,
            self.enableTrading,
            self.feeCurrency, 
            self.isMarginEnabled, 
            self.market,
            self.minFunds, 
            self.name, 
            self.priceIncrement,
            self.priceLimitRate,
            self.quoteCurrency,
            self.quoteIncrement,
            self.quoteMaxSize, 
            self.quoteMinSize, 
            self.symbol
        )
    




class ConfigEntity(Base):
    __tablename__ = "configs"
    symbol = Column("symbol",String , primary_key=True)
    name = Column("name",String)
    increase = Column("increase",Float)
    decrease = Column("decrease",Float)
    funds  = Column("funds  ",Float)

    def __init__(self , symbol=None , name=None , increase=None , decrease =None , funds = None ):
        self.symbol = symbol
        self.name = name
        self.increase = increase
        self.decrease = decrease
        self.funds = funds  
          

    def __repr__(self):
        return "<ConfigEntity (name='%s')>" % (
            self.name
        )
    
    def from_domain(self,model : Config):
            self.symbol= model.symbol
            self.name= model.name
            self.increase= model.increase
            self.decrease= model.decrease
            self.funds  = model.funds  
       

    def to_domain(self):
        return Config(
            self.symbol,
            self.name,
            self.increase,
            self.decrease,
            self.funds              
        )



class ActionEntity(Base):
    __tablename__ = "actions"
    id = Column("id",String ,  primary_key=True)
    symbol = Column("symbol",String)
    timestamp = Column("timestamp", Float)
    direction = Column("direction",String)
    amount = Column("amount",Float)
    price = Column("price",Float)
    profit  = Column("profit  ",Float)
    profit_percent  = Column("profit_percent  ",Float)

    def __init__(self , id= None , symbol=None ,timestamp=None, direction=None , amount=None , price =None , profit = None, profit_percent = None ):
        self.id = id
        self.symbol = symbol
        self.timestamp = timestamp
        self.direction = direction
        self.amount = amount
        self.price = price
        self.profit = profit  
        self.profit_percent =profit_percent
          

    def __repr__(self):
        return "<ConfigEntity (direction='%s')>" % (
            self.direction
        )
    
    def from_domain(self,model : Action):
            self.id = model.id
            self.symbol= model.symbol
            self.timestamp = model.timestamp
            self.direction= model.direction
            self.amount= model.amount
            self.price= model.price
            self.profit  = model.profit 
            self.profit_percent = model.profit_percent 
       

    def to_domain(self):
        return Action(
            self.id,
            self.symbol,
            self.timestamp,
            self.direction,
            self.amount,
            self.price,
            self.profit,
            self.profit_percent             
        )
