###########################################################################
# config.py
###########################################################################

import time, os, logging
from logging.handlers import RotatingFileHandler

def log( log_folder ):
    handler = RotatingFileHandler(
        "{}/app.log".format( log_folder ), 
        maxBytes=2_000_000, 
        backupCount=3
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

class Config():

    def root_dir( self ):
        return( "{}/..".format( os.path.abspath(os.path.dirname(__file__))) )

    def __timestamp( self ):
        timestamp = time.time()
        filename = "{}/data/timestamp.txt".format( self.root_dir() )        
        try: return( open(filename).read().replace('\n', '') )
        except: pass
        return( "" )

    def __is_debug( self ):
        try:
            if( os.environ.get('DEBUG') ):
                return( True )
        except: return( False )

    def test_data( self ):
        self.data["test"]   = True
        self.data["port"]   = 5000
        self.data["domain"] = "http://localhost:{}".format(self.data["port"])       

    def __init__( self ):
        self.data = {
            "test"             : False,
            "language"         : "DE",
            "host"             : "127.0.0.1",
            "port"             : "8005",
            "debug"            : self.__is_debug(),
            "timestamp"        : self.__timestamp(),
            "timeout_refresh"  : 60*1000,
            "big_images"       : False,
            "error"            : "",
            "cache"            : False,
            "tmp_folder"       : "/tmp",
            "log_folder"       : "/tmp",
            "data_folder"      : "{}/data".format( self.root_dir() ),
            "template_folder"  : "{}/data/template".format( self.root_dir() ),
            "schema_folder"    : "{}/data/schema".format( self.root_dir() ),
            "fonts_folder"    : "{}/data/fonts".format( self.root_dir() ),
            "static_folder"    : "{}/docs".format( self.root_dir() ),
            "images_folder"    : "{}/docs/images".format( self.root_dir() ),
            "root_dir"         : self.root_dir(),
            "domain"           : '',
            "db"               : {
                "user"      : "gold", 
                "password"  : "rodengold",
                "host"      : "localhost",
                "database"  : "gold"
            },
            "level"            : {
                "blocked"      : "0",
                "registered"   : "10",
                "payer"        : "20",
                "editor"       : "30",
                "admin"        : "40"
            },
            "accounts"         : [
                { "username" : "hostmaster", "password" : "PC-1715" },
            ],
            "list_materials"   : [
                "gold", "silver", "copper", "platinum", "palladium",
                "butter", "cheese", "bitcoin", "ethereum", "solana", 
                 "cpi", "fed_funds", "treasury_1y", "treasury_2y", 
                 "treasury_5y", "treasury_10y", "treasury_30y", 
            ],
            "smtp_host"        : 'smtp.gmail.com',
            "smtp_port"        : '465',
            "smtp_uid"         : 'roberto.santana.berlin@gmail.com',
            "smtp_pwd"         : 'woim qdex xlhe skdg',
            
            "sms_url"          : 'https://www.teammessage.de/api/v1',
            "sms_id"           : 202927,
            "sms_email"        : 'goldfisher@tmsg.de',
            "sms_token"        : '3fc398e1acc713116a387298ff03b04ba7c98df88c93f8c9cfbf79c4856649f2',
        }
        if( os.environ.get("TEST") != None ): self.test_data()
        self.data["web"] = self.data["domain"]
        
    def config( self ):
        return( self.data )
    
    def log_folder( self ):
        return( self.data["log_folder"] )

    def host( self ):
        return( self.data["host"] )
    
    def port( self ):
        return( self.data["port"] )
    
    def debug( self ):
        return( self.data["debug"] )
    
    def template_folder( self ):
        return( self.data["template_folder"] )
    
    def static_folder( self ):
        return( self.data["static_folder"] )    
    
if __name__ == "__main__":
    pass

# end-of-file
