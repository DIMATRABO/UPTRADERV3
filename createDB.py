from gate_way.alchemy_db_create import Db_creator
from gate_way.config_handler import Config_handler


config = Config_handler()
pg = Db_creator(config)
pg.create()


