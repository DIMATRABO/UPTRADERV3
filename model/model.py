from enum import Enum
from typing import List
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json


@dataclass
class Symbol:
    baseCurrency: str = None            
    baseIncrement: str = None  
    baseMaxSize: str = None 
    baseMinSize: str = None  
    enableTrading: bool = None
    feeCurrency: str = None 
    isMarginEnabled: bool = None  
    market: str = None 
    minFunds: str = None
    name: str = None                     
    priceIncrement: str = None   
    priceLimitRate: str = None
    quoteCurrency: str = None  
    quoteIncrement: str = None 
    quoteMaxSize: str = None
    quoteMinSize: str = None   
    symbol: str = None    

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)



@dataclass
class Config:
    symbol: str = None 
    name : str = None 
    increase : float = None 
    decrease : float = None 
    funds : float = None 

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

@dataclass
class Action:
    id : str = None 
    symbol: str = None 
    timestamp: float = None
    direction : str = None 
    amount : float = None 
    price : float = None 
    profit : float = None
    profit_percent : float =None 


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

class Part:
    def __init__(self , symbol = None , increase = None, decrease = None , funds = None , min_price= None , max_price = None , is_bought = None , buy_price = None , amount = None ):
        self.symbol = symbol 
        self.increase = increase
        self.decrease=decrease
        self.funds= funds  
        self.min_price = min_price
        self.max_price = max_price
        self.is_bought = is_bought
        self.buy_price = buy_price
        self.amount = amount

class Bot:
    def __init__(self):
        self.is_runing = False
        self.stop_event = None


default_conf = Config(
    symbol=None,
    name="Default",
    increase=3,
    decrease=3,
    funds= 10   
)