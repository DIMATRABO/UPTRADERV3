from flask import Flask
from controllers.website.website import websiteController
from controllers.api.symbols import symbolsController
from flask_bcrypt import Bcrypt
from gate_way.config_handler import Config_handler
from model.flaskalchemy import  db

config = Config_handler()



app = Flask(__name__)
dbname = config.get_db_name()
user = config.get_db_user()
password = config.get_db_passwd()
port = config.get_db_port()
host = config.get_db_host()
app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql+psycopg2://"+user+":"+password+"@"+host+":"+str(port)+"/"+dbname
app.config["SECRET_KEY"] = "super-secret-jwt-secret-key-to-change-later"


bcrypt = Bcrypt(app)



app.register_blueprint(websiteController,url_prefix = "/web" )
app.register_blueprint(symbolsController , url_prefix = "/api/symbols") 

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True , port=5454)
