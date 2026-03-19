### begin srv/gold

import sys, os, requests, pdfkit, base64, logging
import lib.Client, lib.Output, lib.Cache, lib.File, lib.Info
from flask import Blueprint, jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

info = Blueprint( "info", __name__, url_prefix="/srv/info/" )

out = lib.Output.Output()
auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)

@info.before_request
@auth.login_required
def before_info():
    pass

@auth.verify_password
def verify_password(username, password):    
    return lib.Client.Client().check(username, password)

@info.route("/", methods=["GET"])
def index_get():
    if "text/html" in lib.Utils.get_accept():
        g.output["info_list"] = lib.Info.Info().get_info_list()
        g.output["mask_schema"] = lib.File.File().get_schema("info", "input")
        return( out.html("info") )        
    errorstr = "Modul 'info' Route '/' Method 'GET' }"
    logger.error( "index_get: {}".format(errorstr) )
    return( lib.Utils.error(400) )

@info.route("/list/", methods=["GET"])
def index_list():        
    if "text/html" in lib.Utils.get_accept():
        g.output["info_list"] = lib.Info.Info().get_info_list()
        return( out.html("info/list") )
    errorstr = "Modul 'info' Route '/' Method 'POST' }"
    logger.error( errorstr )
    return( lib.Utils.error(400) )

def get_html_pdf( url ):
    try:
        html = requests.get(url).text
        pdf = pdfkit.from_string(html, False)
        return( html, base64.b64encode(pdf) )
    except: pass
    return( "","" )

@info.route("/<id>/", methods=["DELETE"])
def index_delete( id ):
    if "text/html" in lib.Utils.get_accept():        
        lib.Info.Info().delete(id)
        g.output["info_list"] = lib.Info.Info().get_info_list()
        return( out.html("info/list") )    
    errorstr = "Modul 'info' Route '/<id>/' Method 'DELETE' }"
    logger.error(errorstr )
    return( lib.Utils.error(400) )

@info.route("/", methods=["PUT"])
def index_put():
    if "text/html" in lib.Utils.get_accept():  
        data = {
            "title"     : request.form.get("title"),
            "url"       : request.form.get("url"),
            "comment"   : request.form.get("comment"),
            "content"   : "",
            "pdf"       : ""
        }
        ( data["content"], data["pdf"] ) = get_html_pdf(data["url"])

        if request.form.get("id") == "":
            id = lib.Info.Info().insert( data )            
        else:
            data["id"] = request.form.get("id")            
            lib.Info.Info().update( data )
            id = data["id"]

        g.output["mask_schema"] = lib.File.File().get_schema("info", "input")
        g.output["refresh_list"] = True
        list = lib.Info.Info().get_info(id)
        for i in ["id", "day", "clock", "title", "url", "comment" ]:            
           g.output[i] = list[i]        
        
        return( out.html("info/mask") )                
    errorstr = "Modul 'info' Route '/' Method 'PUT' }"
    logger.error( "Modul 'info' Route '/' Method 'PUT' }" )
    return( lib.Utils.error(400) )
# end index_put

### end-of-file
