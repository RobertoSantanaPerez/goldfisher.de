#!/usr/bin/env python

###########################################################################
# Application gold
###########################################################################

import os.path, htmlmin, time, json, base64, re, logging
import lib.Config, lib.Output, lib.Client, lib.Utils, lib.Gold, lib.ExchangeRate, lib.Shipping

from flask import g, Flask, Blueprint, render_template, redirect, request, make_response, send_from_directory, Response, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from pathlib import Path
from lib.Config import log

from srv.variety import variety
from srv.gold import gold
from srv.info import info

out = lib.Output.Output()
log( lib.Config.Config().log_folder() )
logger = logging.getLogger(__name__)

app = Flask( __name__,
  template_folder = lib.Config.Config().template_folder(),
  static_folder   = lib.Config.Config().static_folder()
)

@app.before_request
def before_request_func():
    g.config = lib.Config.Config().config()
    g.output  = {}
    g.stash   = {}    

app.register_blueprint( variety )
app.register_blueprint( gold )
app.register_blueprint( info )

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return lib.Client.Client().check(username, password)

@app.route("/jss/<path:path>", methods=['GET'])
def jss_dir(path):
    return send_from_directory("docs/jss", path)

@app.route("/css/<path:path>", methods=['GET'])
def css_dir(path):
    return send_from_directory("docs/css", path)

@app.route("/img/<path:path>", methods=['GET'])
def img_dir(path):
    return send_from_directory("docs/img", path)

@app.route("/favicon.ico", methods=['GET'])
def ico_dir():
    return send_from_directory("docs", "favicon.ico")


@app.errorhandler( 400 )
def bad_request(e):
    return( lib.Utils.error(400) )

@app.errorhandler( 404 )
def page_not_found(e):
    return( lib.Utils.error(404) )
    
@app.route( '/', methods=["GET"] )
def index():    
    return( out.html("index") )

@app.route( '/dashboard/', methods=["GET"] )
@auth.login_required
def dashboard():        
    if "text/html" in lib.Utils.get_accept():
        return( out.html("dashboard") )
    return( bad_request("") )

@app.route( '/error/<msg>/', methods=["GET"] )
def error( msg ):
    logger.error( "Browser: " + msg )
    if "application" in lib.Utils.get_accept():
        return(out.json({
            "data"      : {}, 
            "success"   : True,
            "errorstr"  : ""
         }))
    return( "<html><body>success: True</body>/html>" )


@app.route( '/srv/title/', methods=["GET"] )
# no auth, index-site don't without
def srv_title():
    if "application/json" in lib.Utils.get_accept():
        ( local_day, local_clock ) = lib.Utils.get_current_day_clock()
        ( current, last ) = lib.Gold.Gold().get_current_last_price()
        if ( current > last ): trend = "🡅"
        elif ( current < last ): trend = "🡇"
        else: trend = ""
        return( out.json({
            "data" : {
                "local-date": local_day,
                "local-time": local_clock,
                "current"   : str( current ),
                "trend"     : trend,
            }
        }) )  
    else: return( bad_request("") )
# srv/title/

@app.route( '/schema/<service>/<filename>/', methods=["GET"] )
@auth.login_required
def schema_srv_file(service, filename):
    if "application/json" in lib.Utils.get_accept():
        dir = Path(g.config["schema_folder"])                   
        if dir.exists() and dir.is_dir():
            subdir = Path("{}/{}".format(g.config["schema_folder"], service))
            if subdir.exists() and subdir.is_dir():
                fn = "{}/{}/{}.json".format(g.config["schema_folder"], service, filename)
                file = Path(fn)
                if file.exists() and file.is_file():
                    try:
                        with open(fn, "r", encoding="utf-8") as f:
                            data = json.load(f)                   
                        return( out.json({
                            "data": data, 
                            "success" : True,
                            "errorstr" : ""
                        }) )
                    except Exception as e:
                        errorstr = "Cannot read schema file: {}".format(str(e))
                        logger.error( "HTTP Error: {}".format(errorstr) )
                        return( out.json({
                            "data": {}, 
                            "success" : False,
                            "errorstr" : errorstr
                        }) )
    else: return( bad_request("") )

if __name__ == "__main__":
    app.run(
        host  = lib.Config.Config().host(),
        port  = lib.Config.Config().port(),
        debug = lib.Config.Config().debug()
    )
    
### eof