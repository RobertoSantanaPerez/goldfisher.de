###############################################################################
#
# Variety.pm
#
###############################################################################
from flask import g
import time, json, requests, logging
import lib.MySQL, lib.Utils, lib.Config

logger = logging.getLogger(__name__)
config = lib.Config.Config().config()

class Variety( lib.MySQL.Mysql ):

    def __init__( self ):
        super().__init__()
        pass
    
    def get_materials( self ):
        return( config["list_materials"])

    def check_material( self, material ):
        for m in config["list_materials"]:
            if m == material: return( m )
        return( False )

    def get_variety_api( self ):
        try:
            json_data = requests.get('https://data.silv.app/commodities.json')            
            data = json_data.json()
            prices = {}
            for m in self.get_materials():                
                prices[m] = data["commodities"][m]["price"]   
            return( prices )
        except Exception as e:
            errorstr = "can't read from data.silv.app/commodities.json: {}".format(str(e))
            logger.info( "HTTP Error: {}".format(errorstr) )
        return( False )

    def insert( self ):                  
        ( day, clock ) = lib.Utils.get_current_day_clock()        
        data =  self.get_variety_api()        
        if data == False: return( False )
        self.transaction()
        self.cursor.execute(
            "SELECT id FROM variety WHERE day=%s AND clock=%s",
            [ day, clock ]
        )
        if self.cursor.rowcount == 0 :
            self.cursor.execute(
                "INSERT INTO variety SET day=%s, clock=%s, gold=%s, " +
                " copper=%s, silver=%s, platinum=%s, palladium=%s," +
                " butter=%s, cheese=%s, treasury_10y=%s, treasury_1y=%s, treasury_2y=%s, " +
                " treasury_5y=%s, treasury_30y=%s, fed_funds=%s, " +
                " cpi=%s, bitcoin=%s, ethereum=%s, solana=%s",
                [   day, clock, data["gold"], data["copper"], data["silver"], 
                    data["platinum"], data["palladium"], 
                    data["butter"], data["cheese"], data["treasury_10y"], data["treasury_1y"], 
                    data["treasury_2y"], data["treasury_5y"], data["treasury_30y"], 
                    data["fed_funds"], data["cpi"], data["bitcoin"],
                    data["ethereum"], data["solana"]
                ]
            )
        self.commit()

    def get_price_current( self, material ):
        (day, clock) = lib.Utils.get_current_day_clock()
        material = self.check_material( material )
        if(material == False ): return( False )
        
        try: 
            self.cursor.execute(
                "SELECT "+material+" FROM variety ORDER BY day DESC, clock " 
                + " DESC LIMIT 1"
            )
            if self.cursor.rowcount > 0 :
                price, = self.cursor.fetchone() 
                return( price )
        except: pass
        return( False )


    def get_current_last_price( self, material ):        
        material = self.check_material( material )
        if(material == False ): return( False )
        self.cursor.execute(
            "SELECT "+material+" FROM variety "
            + " ORDER BY day DESC, clock DESC "
            + "LIMIT 1"
        )
        current = self.cursor.fetchone()
        self.cursor.execute(
            "SELECT "+material+" FROM variety "
            + " ORDER BY day DESC, clock DESC "
            + "LIMIT 1,1"
        )
        last = self.cursor.fetchone()        
        return( current[0], last[0] )

    def get_day_prices( self, day, material ):
        material = self.check_material( material )
        if(material == False ): return( False )
        list_price = lib.Utils.get_all_clock_for_day_variety()
        self.cursor.execute(
            "SELECT day, clock, "+material+" FROM variety "
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
    
    def get_current_day_prices( self, material ):
        day = lib.Utils.get_current_day()
        return( self.get_day_prices(day, material) )
    
# end-of-file
