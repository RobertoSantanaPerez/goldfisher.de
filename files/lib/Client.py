import lib.Config, lib.MySQL
from flask import g
import hashlib

config = lib.Config.Config().config()

class Client( lib.MySQL.Mysql ):
      
    def __init__( self ):
        super().__init__()
        pass

    def check( self, username, password ):
        if ( username == "" ): return
        if ( password == "" ): return
        self.cursor.execute(
            "SELECT id, uid, level FROM client WHERE  uid=%s AND pwd=%s LIMIT 1",
            [ username, hashlib.md5(password.encode('utf-8')).hexdigest() ]
        )
        if self.cursor.rowcount > 0 :
            g.stash["client_id"], g.stash["client_uid"], g.stash["client_level"], = self.cursor.fetchone() 
            g.output["client_name"] = g.stash["client_uid"]
            if g.stash["client_level"] >= config["level"]["editor"]:
                g.output["right_for_info"] = True
            if g.stash["client_level"] >= config["level"]["payer"]:
                g.output["right_for_current"] = True
                g.output["right_for_view"] = True

            return( True )
        return

    def list_clients( self ):
        list = []
        self.cursor.execute(
            "SELECT id, uid, email, level, limitbuy, limitsell FROM client"            
        )                
        for row in self.cursor.fetchall():          
            list.append({
                "id"        : row[0],
                "uid"       : row[1],
                "email"     : row[2],
                "level"     : row[3],
                "limitbuy"  : row[4],
                "limitsell" : row[5]
            })
        return( list )


    def add_client( self, param ):
        try:
            self.transaction()
            self.cursor.execute(
                "INSERT INTO client SET uid=%s, email=%s, level=%s, pwd=%s",
                [ 
                    param["uid"], param["email"], param["level"],
                    hashlib.md5(param["pwd"].encode('utf-8')).hexdigest()
                ]
            )            
            self.commit()
            return( True )
        except Exception as e:
            print(e)
        return( False )
    
    def del_client( self, param ):
        try:
            self.transaction()
            self.cursor.execute(
                "DELETE FROM client WHERE uid=%s",
                [ param["uid"] ]
            )
            self.commit()
            return( True )
        except Exception as e:
            print(e)
        return( False )
    
    def email_client( self, param ):
        try:
            self.transaction()
            self.cursor.execute(
                "UPDATE client SET email=%s WHERE uid=%s",
                [ param["email"], param["uid"] ]
            )
            self.commit()
            return( True )
        except Exception as e:
            print(e)
        return( False )
    
    def status_client( self, param ):
        try:
            self.transaction()
            self.cursor.execute(
                "UPDATE client SET level=%s WHERE uid=%s",
                [ param["level"], param["uid"] ]
            )
            self.commit()
            return( True )
        except Exception as e:
            print(e)
        return( False )
    
    def credit_client( self, param ):
        try:
            self.transaction()
            self.cursor.execute(
                "UPDATE client SET credit=credit+%s WHERE uid=%s",
                [ param["credit"], param["uid"] ]
            )
            self.commit()
            return( True )
        except Exception as e:
            print(e)
        return( False )
# end class Passwd

if __name__ == "__main__":
    pass

# end-of-file