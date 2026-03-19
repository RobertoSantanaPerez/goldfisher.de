### begin srv/gold

import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import lib.Client, lib.Output, lib.Cache
from flask import Blueprint, jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

gold = Blueprint( "gold", __name__, url_prefix="/srv/gold/" )

out = lib.Output.Output()
auth = HTTPBasicAuth()

@gold.before_request
@auth.login_required
def before_goldapi():
    pass

@auth.verify_password
def verify_password(username, password):    
    return lib.Client.Client().check(username, password)

@gold.route("/", methods=["GET"])
def index():
    return( lib.Utils.http_error(404) )

@gold.route( '/current/', methods=["GET"] )
def current():
    if "text/html" in lib.Utils.get_accept():
        g.output["day"] = ""    
        return( out.html("gold-price-day") )
    elif "application/json" in lib.Utils.get_accept():
        gold = lib.Gold.Gold()
        price = gold.get_price_current()
        price = price if price != False else "undef"
        (list_price, min, max, average) = gold.get_current_day_prices()        
        ( day, clock ) = lib.Utils.get_current_day_clock()
        rate = lib.ExchangeRate.Rate()
        exchangerate = rate.get_current_exchangerate()
        return( out.json({
            "data" : {            
                "local-date"        : day,
                "local-time"        : clock,
                "amount"            : str(price),
                "currency"        : "USD", 
                "date"              : day,
                "time"              : clock,
                "list_price"        : list_price,                
                "min"               : min,
                "max"               : max,
                "average"           : average,
                "rate"              : str( exchangerate ) if exchangerate != False else "",
                "info"              : "data complete"
            }
        }) )
    else:         
        errorstr = "Route '/current/' Method 'GET' }"
        app.logger.info( "HTTP Error: {}".format(errorstr) )
        return( lib.Utils.error(400) )
# end current

@gold.route( '/day/<day>/', methods=["GET"] )
def day( day ): 
    if "text/html" in lib.Utils.get_accept():
        g.output["day"] = day
        return( out.html("gold-price-day") )
    elif "application/json" in lib.Utils.get_accept():
        gold = lib.Gold.Gold()
        price = gold.get_price_current()
        price = price if price != False else "undef"
        (list_price, min, max, average) = gold.get_day_prices( day )    
        rate = lib.ExchangeRate.Rate()
        exchangerate = rate.get_exchangerate( day )
        data = {
            "data" : {
                "amount"            : "",
                "currency"          : "", 
                "date"              : day,
                "time"              : "",
                "list_price"        : list_price,
                "min"               : min,
                "max"               : max,
                "rate"              : str( exchangerate ) if exchangerate != False else "",
                "info"              : "data complete"
            }
        }        
        return( out.json(data) )
    else: 
        errorstr = "Route '/day/<day>/' Method 'GET' }"
        app.logger.info( "HTTP Error: {}".format(errorstr) )
        return( lib.Utils.error(400) )
# end day

@gold.route( '/week/<year>/<week>/', methods=["GET"] )
def week( year, week ):
    if "text/html" in lib.Utils.get_accept():
        g.output["year"] = year
        g.output["week"] = week
        return( out.html("gold-price-week") )    
    elif "application/json" in lib.Utils.get_accept():
        cache = lib.Cache.Cache( year + week )  
        cache.kill()
        cache_data = cache.read()
        if( cache_data != None ):
            return( out.json(cache_data) )
        
        days = lib.Utils.days_from_week( year, week )
        day_list = []
        for day in days :
            (list_price, min, max, average)= lib.Gold.Gold().get_day_prices( day )
            day_list.append({
                "day"  : day,
                "min"  : min,
                "max"  : max,
                "list" : list_price
            })
        data = {
            "data" : {
                "year"  : year,
                "week"  : week,
                "list"  : day_list,
                "info"  : "data complete"
            }
        }
        cache.write( data )    
        return( out.json(data) )
    else: 
        errorstr = "Route '/week/<year>/<week>/' Method 'GET' }"
        app.logger.info( "HTTP Error: {}".format(errorstr) )
        return( lib.Utils.error(400) )        
# end week

### end-of-file
