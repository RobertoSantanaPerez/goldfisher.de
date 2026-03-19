###########################################################################
# Modul: File.py einlesen von Festplatte 
###########################################################################
from flask import g
from pathlib import Path
import json, logging, lib.Output

out = lib.Output.Output()


class File():

    def __init__( self ):        
        pass

    def _check_folder( self, name ):
        dir = Path( name )
        if dir.exists() and dir.is_dir():
            return( True )
        return( False )
    
    def _check_file( self, name ):
        file = Path( name )
        if file.exists() and file.is_file():
            return( True )
        return( False )
      
    def get_schema( self, service_name, file_name ):
        if not( self._check_folder(g.config["schema_folder"]) ) :
            errorstr = "dir {} not found".format(g.config["schema_folder"])
            logger.error( errorstr )
            return( out.json({
                "data": {}, 
                "success" : False,
                "errorstr" : errorstr
            }) )
   
        service_dir = Path("{}/{}".format(g.config["schema_folder"], service_name))
        if not( self._check_folder(service_dir) ) :
            errorstr = "dir {} not found".format( "{} not found".format( service_dir ) )
            logger.error( errorstr )
            return( out.json({
                "data": {}, 
                "success" : False,
                "errorstr" : errorstr
            }) )     

        json_name = "{}/{}/{}.json".format(g.config["schema_folder"], service_name, file_name)
        if not( self._check_file(json_name) ) :
            errorstr = "File {} not found".format( json_name )
            logger.error( errorstr )
            return( out.json({
                "data": {}, 
                "success" : False,
                "errorstr" : errorstr
            }) )                        
        try:
            with open(json_name, "r", encoding="utf-8") as file:
                data = json.load(file)
            return({
                "data": data, 
                "success" : True,
                "errorstr" : ""
            })
        except Exception as e:
            errorstr = "Cannot read schema file: {}".format(str(e))
            logger.error( "Error: {}".format(errorstr) )
            return( out.json({
                "data": {}, 
                "success" : False,
                "errorstr" : errorstr
            }) ) 
        
        errorstr = "unknow error"
        logger.error( "Error: {}".format(errorstr) )
        return( out.json({
            "data": {}, 
            "success" : False,
            "errorstr" : errorstr
        }) ) 


if __name__ == "__main__":    
    pass

# end-of-file