from flask import Blueprint 
from views import views
from gate_way.log import Log
import gate_way.kucoin_api as kucoin
from flask import request
from model.model import *
from use_cases.symbol.save import Save
from use_cases.symbol.delete_list import Delete
from use_cases.symbol.getAll import GetAll
from use_cases.symbol.inputs.getAllInput import GetAllInput
from gate_way.symbol.sqlalchimyRepo import SqlAlchimy_repo as Symbol_repo

from use_cases.config.save import Save as SaveConfig
from use_cases.config.delete import Delete as DeleteConfig
from use_cases.config.getAll import GetAll as GetAllConfig
from gate_way.config.sqlalchimyRepo import SqlAlchimy_repo as Config_repo

from gate_way.action.sqlalchimyRepo import SqlAlchimy_repo as Action_repo
from use_cases.action.getAllSymbol import GetAll as GetActionsBySymbol

from use_cases.bot.start import Start
import json


bot_model = Bot()

parts = []

saving_handler = Save(Symbol_repo())
delete_handler = Delete(Symbol_repo())
getAll_handler = GetAll(Symbol_repo())

config_saving_handler = SaveConfig(Config_repo())
getAllConfigs_handler = GetAllConfig(Config_repo())

getActionBySymbol = GetActionsBySymbol(Action_repo())

stat_bot_handler = Start(symbolRepo=Symbol_repo() , configRepo=Config_repo())

websiteController = Blueprint("websiteController", __name__)
logger = Log()


@websiteController.route('/', methods=['GET'])
def index():
    return views.landing_page()



@websiteController.route('/dashboard', methods=['GET'])
def dashboard():
    return views.dashboard()


@websiteController.route('/symbols', methods=['GET'])
def symbols():
    data = kucoin.get_symbols()['data']
    bots_data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    return views.symbols(data = data , bots_data=bots_data)


@websiteController.route('/addsymbols', methods=['POST'])
def addsymbols():
    selected_indices = request.form.getlist('selected_indices')
    data = kucoin.get_symbols()['data']
    for symbol in data:
    
        if symbol["symbol"] in selected_indices[0]:
            new_symbol = Symbol(
                    baseCurrency= symbol["baseCurrency"],           
                    baseIncrement= symbol["baseIncrement"], 
                    baseMaxSize= symbol["baseMaxSize"],
                    baseMinSize= symbol["baseMinSize"], 
                    enableTrading= symbol["enableTrading"], 
                    feeCurrency= symbol["feeCurrency"],
                    isMarginEnabled= symbol["isMarginEnabled"],  
                    market= symbol["market"],
                    minFunds= symbol["minFunds"], 
                    name= symbol["name"],                    
                    priceIncrement= symbol["priceIncrement"],  
                    priceLimitRate= symbol["priceLimitRate"], 
                    quoteCurrency= symbol["quoteCurrency"], 
                    quoteIncrement= symbol["quoteIncrement"],
                    quoteMaxSize= symbol["quoteMaxSize"], 
                    quoteMinSize= symbol["quoteMinSize"],  
                    symbol= symbol["symbol"],
            )
            saving_handler.handel(new_symbol)
    
    bots_data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    return views.symbols(data = data , bots_data=bots_data)



@websiteController.route('/removesymbols', methods=['POST'])
def removesymbols():
    selected_indices = json.loads(request.form.getlist('selected_indices')[0])
    data = kucoin.get_symbols()['data']
    delete_handler.handel(selected_indices)
    bots_data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    return views.symbols(data = data , bots_data=bots_data)




@websiteController.route('/configurations', methods=['GET'])
def configurations():
    bots_data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    configs = [ sym.to_dict() for sym in getAllConfigs_handler.handle(getconfigsInput=GetAllInput(all="all"))]
    return views.configurations(bots_data=bots_data , configs = configs )


@websiteController.route('/saveconfig', methods=['POST'])
def saveconfig():
    config = Config()
    config_from_request = request.form.items()

    for  key, value in   config_from_request : 
        if key == "config_name":
            config.name = value
        if key == "symbol":
            config.symbol = value
        if key == "percent_increase":
            config.increase = value
        if key == "percent_decrease":
            config.decrease = value
        if key == "percent_funds":
            config.funds = value

    config_saving_handler.handel(config=config)
    
    bots_data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    configs = [ sym.to_dict() for sym in getAllConfigs_handler.handle(getconfigsInput=GetAllInput(all="all"))]
    return views.configurations(bots_data=bots_data , configs = configs )

    
@websiteController.route('/bot', methods=['GET'])
def bot():
    data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    return views.bot(bot = bot_model , data=data )


@websiteController.route('/symbolbot/<symbol>', methods=['GET'])
def symbolbot(symbol):
    actions = getActionBySymbol.handle(symbol=symbol)
    total_actions = 0
    pnl = 0
    for action in actions:
        if not action.profit is None:
            pnl +=  action.profit
        total_actions +=1     

    return views.symbolbot(bot = bot_model , symbol = symbol , actions = actions , pnl = pnl , total_actions = total_actions )


@websiteController.route('/runbot', methods=['GET'])
def runbot():
    bot_model.is_runing = True
    stat_bot_handler.handel(bot = bot_model , parts = parts)
    data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    return views.bot(bot = bot_model , data=data)


@websiteController.route('/stopbot', methods=['GET'])
def stopbot():
    bot_model.stop_event.set()
    data = [ sym.to_dict() for sym in getAll_handler.handle(getsymbolsInput=GetAllInput(all="all"))]
    bot_model.is_runing  = False
    return views.bot(bot = bot_model , data=data)