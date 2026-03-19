### begin-of-file

import os, sys, json, inspect, hashlib
from pathlib import Path
from flask import g

class Cache():

  def __init__( self, param ):
    methodname = sys._getframe(1).f_code.co_name
    filename = inspect.stack()[1].filename
    string = "{}::{}::{}".format(
      filename, methodname, 
      json.dumps(param, sort_keys=True)
    )    
    self.name = "{}/{}.cache".format(
      g.config["tmp_folder"], 
      hashlib.sha256(string.encode()).hexdigest()
    )
  
  def write( self, data ):
    if( g.config["cache"] != True ): return( None )
    try:
      with open( self.name, 'w', encoding="utf-8" ) as f:
        print( json.dumps( data ), file=f )  
        f.close()
        return( True )
    except: pass
    return( False )
  
  def read( self ):  
    if( g.config["cache"] != True ): return( None )
    try:
      with open( self.name, "r", encoding="utf-8" ) as f:
        return( json.load(f) )
    except: pass
    return( None )
  
  def kill( self ):
    try:
      for files in Path(g.config["tmp_folder"]).glob("*.cache"):
        files.unlink()
      return( True )
    except: pass
    return( False )

# end class Cache

if __name__ == "__main__":
  pass

### end-of-file