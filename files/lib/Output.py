import os, sys, json
from flask import Response, make_response, jsonify, render_template, g
class Output:

    def __init__( self ):
        self.headers = {}
        pass
    # end __init__

    def header( self, key, value ):
        self.headers[key] = value        

    def config_to_output( self ):
        for w in [
            "test", "language", "domain", "web", 
            "timeout_refresh", "timestamp",
            "list_materials"
        ]:
            g.output[w] = g.config[w]
        self.headers = {}
    
    def html( self, filename ):
        self.config_to_output()
        original = render_template(
            "{}.html".format( filename ),
            **g.output
        )
        response = make_response( original )  
        response.mimetype = "text/html"
        for h in self.headers.keys():
           response.headers[h] = self.headers[h]
        self.headers = {}
        return( response )        
    # end html

    def json( self, data ):
        response = make_response(jsonify(data))        
        response.mimetype = "application/json"
        for h in self.headers.keys():
           response.headers[h] = self.headers[h]
        self.headers = {}
        return( response )
    # end json

# end class Output

if __name__ == "__main__":
    pass

# end-of-file