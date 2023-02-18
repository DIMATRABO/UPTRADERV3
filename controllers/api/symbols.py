from flask import Blueprint 
from gate_way.log import Log
import gate_way.kucoin_api  as kucoin

symbolsController = Blueprint("symbolsController", __name__)
logger = Log()


@symbolsController.route('/', methods=['GET'])
def index():
    return kucoin.get_symbols()

