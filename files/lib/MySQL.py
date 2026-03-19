import mysql.connector
import lib.Config

config = lib.Config.Config().config()

class Mysql():

    def __init__( self ):
        self.connection = mysql.connector.connect(
            user        = config["db"]["user"], 
            password    = config["db"]["password"],
            host        = config["db"]["host"],
            database    = config["db"]["database"]
        )        
        self.cursor = self.connection.cursor(buffered=True)
        self.trace =False 
    
    def transaction( self ):
        self.connection.start_transaction()
        if self.trace: print("transaction")

    def commit( self ):
        self.connection.commit()
        if self.trace: print("commit")

    def rollback( self ):
        self.connection.rollback()

    def __del__( self ):
        try: self.cursor.close() 
        except: pass
        try: self.connection.close()
        except: pass
        pass

# end-of-file
