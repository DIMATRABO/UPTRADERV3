from flask import render_template
from gate_way.config_handler import Config_handler

config = Config_handler()



def dashboard():
    return render_template("dashboard.html", app_name = config.get_app_name())

def symbols(data , bots_data):
    return render_template("symbols.html", app_name = config.get_app_name() , data = data , data2 = bots_data)

def configurations(bots_data , configs ):
    config_symbols = [ conf["symbol"] for conf in configs] 
    return render_template("configurations.html" , app_name = config.get_app_name() , data = bots_data , configs= configs , config_symbols=config_symbols)

def bot(bot , data):
    return render_template("bot.html", app_name = config.get_app_name(), bot = bot , data=data)

def symbolbot(bot, symbol , actions , pnl , total_actions ):
    return render_template("symbolbot.html", app_name = config.get_app_name(),bot = bot , symbol = symbol , actions = actions , pnl = pnl , total_actions = total_actions )


