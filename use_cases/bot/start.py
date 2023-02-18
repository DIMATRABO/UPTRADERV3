from model.model import *
from  gate_way.kucoin_api import * 
from gate_way.kucoin_websockets import *
from gate_way.dataBaseSession.sessionContext import SessionContext
from  threading import Thread
import queue

class Start:
    def __init__(self, symbolRepo , configRepo ):
        self.symbolRepo = symbolRepo
        self.configRepo = configRepo
        self.sessionContext = SessionContext()

    def initialize_min_prices(self , paires , configs):
        parts = []
        config_symbols = [ conf.symbol for conf in configs] 
        for paire in paires:
            if paire.symbol in config_symbols:
                index = config_symbols.index(paire.symbol)
                current_price = get_price(paire.symbol)
                part = Part( 
                        symbol= paire.symbol ,
                        increase=configs[index].increase,
                        decrease=configs[index].decrease,
                        funds=configs[index].funds,
                        min_price=current_price,
                        max_price=0,
                        is_bought=False)
                parts.append(part)
            else :
               
                current_price = get_price(paire.symbol)
                part = Part( 
                        symbol= paire.symbol ,
                        increase=default_conf.increase,
                        decrease=default_conf.decrease,
                        funds=default_conf.funds,
                        min_price=current_price,
                        max_price=0,
                        is_bought=False)
                parts.append(part)

        return parts


    def handel(self ,bot , parts ):
        with self.sessionContext as session :
            paires = self.symbolRepo.getAllSymbols(session)
            configs = self.configRepo.getAllConfigs(session)
        parts = self.initialize_min_prices(paires, configs)
        part_dict = dict()
        for part in parts :
            part_dict["/market/ticker:"+ part.symbol] = part
        result_queue = queue.Queue()
        thread = Thread(target=start_monitoring , args=( bot , part_dict , result_queue))
        thread.start()
        bot.stop_event = result_queue.get()
  



