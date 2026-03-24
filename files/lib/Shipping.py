##############################################################################
#
# Shipping
#
##############################################################################

import smtplib, requests
import lib.MySQL, lib.Utils, lib.Config
from email.message import EmailMessage

config = lib.Config.Config().config()

def error( msg ):
    print( msg )

class SMS():
    def __init__( self ):
        self.data = {
            "url"   : config["sms"]["url"],
            "id"    : config["sms"]["id"],
            "email" : config["sms"]["email"],
            "token" : config["sms"]["token"],
        }
       
    def ping( self ):
        try:
            response = requests.get(
                "{}/health/".format(self.data["url"] )
            )          
            data = response.json()
            if( response.json()["status"] ):                
                return( True )
            return( False )
        except Exception as e: 
            print("Error: {}".format(e))
            return( False )

    def send( self, param ):
        for key in ["to", "body"]:
            try: param[ key ]
            except:
                error( "Eror: '{}' not defined".format(key) )
                return( False )
        try:            
            response = requests.get( "{}/sms/send/".format(self.data["url"]),
                headers={
                    "Authorization": self.data["token"]
                },
                json={
                    "team_id"           : self.data[ "id" ],
                    "teamlist_email"    : self.data[ "email" ],
                    "message"           : param[ "body" ],
                    "to_mobile"         : param[ "to" ],
                    "test"              : 1
                }
            )                        

            print( self.data[ "id" ], response.json() )
            
            return( True )
        except: return( False )
        
        pass
# end class SMS


class SMTP():
    def __init__( self ):
        self.data = {
            "host"  : config["smtp"]["host"],
            "port"  : config["smtp"]["port"],
            "uid"   : config["smtp"]["uid"],
            "pwd"   : config["smtp"]["pwd"],
        }

    def ping( self ):
        try:    
            with smtplib.SMTP_SSL(self.data["host"], self.data["port"], timeout=10) as server:
                server.ehlo()            
            return( True )
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            return( False )
        except Exception as e:
            return( False )
    # end ping

    def send( self, param ):
        for key in ["to", "subject", "body"]:
            try: param[ key ]
            except:
                error( "Eror: '{}' not defined".format(key) )
                return( False )
        try:
            msg = EmailMessage()
            msg['From'] = self.data["uid"]
            msg['To'] = param["to"]
            msg['Subject'] = param["subject"]
            msg.set_content(param["body"])
            with smtplib.SMTP_SSL( self.data["host"],  self.data["port"]) as server:
                server.login(self.data["uid"], self.data["pwd"])
                server.send_message(msg)
            return( True )
        except Exception as e:
            error( "Eror: '{}' not defined".format(e) )
        return( False )
      
# end class SMTP

# end-of-file
