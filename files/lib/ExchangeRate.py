import time, json, requests
import lib.MySQL, lib.Utils

class Rate( lib.MySQL.Mysql ):

    def __init__( self ):
        super().__init__()        
        pass
    
    def get_datepoint_today( self ):
        now = time.localtime()
        mon = now.tm_mon if now.tm_mon>10 else "0{}".format(now.tm_mon)
        mday = now.tm_mday if now.tm_mday>10 else "0{}".format(now.tm_mday)
        hour = now.tm_hour if now.tm_hour>10 else "0{}".format(now.tm_hour)
        min = now.tm_min if now.tm_min>10 else "0{}".format(now.tm_min)
        datepoint = "{}-{}-{}".format(
            now.tm_year, mon, mday
        ) 
        return( datepoint )

    def get_exchange_rate_api( self, to, date ):
        try:
            json_data = requests.get(
                "https://free.ratesdb.com/v1/rates?from=EUR&to={}&date={}"
                .format( to, date )
            )
            return( json_data.json()["data"]["rates"][to] )            
        except Exception as e:
            errorstr = "get_datepoint_today: {}".format(str(e))
            app.logger.info( "HTTP Error: {}".format(errorstr) )            
        return( False )
   
    def insert_any_day ( self, day ):
        to="usd"                
        rate = self.get_exchange_rate_api(to.upper(), day )
        if rate == False: return( False )
        self.transaction()        
        self.cursor.execute(
            "SELECT id FROM exchangerate WHERE day=%s",
            [ day ]
        )
        if self.cursor.rowcount == 0 :
            self.cursor.execute(
                "INSERT INTO exchangerate SET day=%s, usd=%s",
                [ day, rate ]
            )
        self.commit()
        return( True )
        
    def insert_day ( self ):  
        today = lib.Utils.get_date_today()
        return( self.insert_any_day(today) )     

    def get_exchangerate( self, day ):
        self.cursor.execute(
            "SELECT usd FROM exchangerate WHERE day = %s",
            [ day ]
        )
        if self.cursor.rowcount == 1:
            rate, = self.cursor.fetchone() 
            return( rate )            
        return( False )

    def get_current_exchangerate( self ):
        self.cursor.execute(
            "SELECT usd FROM exchangerate ORDER BY day DESC LIMIT 1",            
        )
        if self.cursor.rowcount == 1:
            rate, = self.cursor.fetchone() 
            return( rate )            
        return( False )

if __name__ == "__main__":
    pass

# end-of-file