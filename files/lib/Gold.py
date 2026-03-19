import time, json, requests
import lib.MySQL, lib.Utils

class Gold( lib.MySQL.Mysql ):

    def __init__( self ):
        super().__init__()        
        pass
    
    def get_gold_api( self ):
        try:
            json_data = requests.get('https://api.gold-api.com/price/XAU')
            return( json_data.json()["price"] )            
        except Exception as e:
            errorstr = "can't read from api.gold-api.com: {}".format(str(e))
            app.logger.info( "HTTP Error: {}".format(errorstr) )
        return( False )

    def insert( self ):          
        ( day, clock ) = lib.Utils.get_current_day_clock()        
        price = self.get_gold_api()
        if price == False: return( False )
        self.transaction()
        self.cursor.execute(
            "SELECT id FROM goldapicom WHERE day=%s AND clock=%s",
            [ day, clock ]
        )
        if self.cursor.rowcount == 0 :
            self.cursor.execute(
                "INSERT INTO goldapicom SET day=%s, clock=%s, price=%s",
                [ day, clock, price ]
            )
        self.commit()

    def get_price( self, day ):        
        return( "undef" )

    def get_price_current( self ):
        (day, clock) = lib.Utils.get_current_day_clock()
        try: 
            self.cursor.execute(
                "SELECT price FROM goldapicom ORDER BY day DESC, clock DESC LIMIT 1"                    
            )
            if self.cursor.rowcount > 0 :
                price, = self.cursor.fetchone() 
                return( price )
        except: pass
        return( False )
     
    def get_current_last_price( self ):
        self.cursor.execute(
            "SELECT price FROM goldapicom "
            + " ORDER BY day DESC, clock DESC "
            + "LIMIT 1"            
        )
        current = self.cursor.fetchone()
        self.cursor.execute(
            "SELECT price FROM goldapicom "
            + " ORDER BY day DESC, clock DESC "
            + "LIMIT 1,1"            
        )
        last = self.cursor.fetchone()        
        return( current[0], last[0] )

    def get_day_prices( self, day ):
        list_price = lib.Utils.get_all_clock_for_day()
        list_derivate = lib.Utils.get_all_clock_for_day()
        prediction = []
        list_prediction = lib.Utils.get_all_clock_for_day()
        self.cursor.execute(
            "SELECT day, clock, price FROM goldapicom "
            + " WHERE day = %s "             
            + " ORDER BY day, clock", 
            [ day ]
        )
        rows = self.cursor.fetchall()
        sum = 0
        min = 0
        max = 0
        average = 0
        last = None
        for row in rows:          
            
            if min == 0 and max == 0:
                min = row[2]
                max = row[2]
            else: 
                if row[2] < min: min = row[2]
                if row[2] > max: max = row[2]
            sum = sum + row[2]

            #fuerende "0" bei Bedarf einsetzen
            clock = lib.Utils.clock_mysql_program( row[1] )            
            list_price[clock] = str( row[2] )            

        if len(rows) > 0: average = sum/len(rows)
        self.cursor.close()
        return( list_price, str(min), str(max), str(average) )
    
    def get_current_day_prices( self ):
        day = lib.Utils.get_current_day()
        return( self.get_day_prices(day) )

# end-of-file
