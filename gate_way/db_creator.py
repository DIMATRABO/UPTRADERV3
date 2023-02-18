from configparser import ConfigParser
import psycopg2
import json

class Db_creator :
    db_schema_file:str
    parser:None
    data:None
    
    dbname:str
    user:str
    password:str
    port:int
    conn: None
    cursor:None

    def __init__(self, config):
        self.parser=ConfigParser()
        self.db_schema_file="../config/db_schema.json"
        with open(self.db_schema_file, "r") as jsonfile:
            self.data = json.load(jsonfile)
        
        
        self.dbname = config.get_db_name()
        self.user = config.get_db_user()
        self.password = config.get_db_passwd()
        self.port = config.get_db_port()
        print(f"dbname={self.dbname} user={self.user} password={self.password} port={self.port}")
        self.conn= psycopg2.connect(f"dbname={self.dbname} user={self.user} password={self.password} port={self.port}")
        self.cursor = self.conn.cursor()


    def create(self):
        try:
            for command in self.data['tables']:
                self.cursor.execute(command)
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error) ## log error
        finally:
            if self.conn is not None:
                self.conn.close()
