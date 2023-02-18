from sqlalchemy import Column, String , DateTime, Float , Boolean, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Symbol(db.Model):
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

    def __init__(self , baseCurrency , baseIncrement, baseMaxSize , baseMinSize, enableTrading, feeCurrency,isMarginEnabled,market,minFunds,name,priceIncrement,priceLimitRate, quoteCurrency,quoteIncrement, quoteMaxSize, quoteMinSize,symbol):
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

