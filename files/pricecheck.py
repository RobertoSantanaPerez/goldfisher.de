#!/usr/bin/env python

from sys import argv
import lib.Config, lib.Client, lib.Gold, lib.Shipping

threshold_for_buy   = 4330.20
threshold_for_sell  = 5000.00

class SendInfo():

    def __init__( self ):
        ( self.current_price, self.last_price ) = lib.Gold.Gold().get_current_last_price()
        self.clients = lib.Client.Client().list_clients()
        self.Email = lib.Shipping.SMTP()
        print("PRICECHECK:", self.current_price)

    def send_sell_info( self ):
        for client in self.clients:            
            if( int(client["level"]) > 20 and
                float(self.last_price) <= float(client["limitsell"]) and 
                float(self.current_price) > float(client["limitsell"])
            ):
                print("Info SELL:", client["uid"], client["limitsell"], self.current_price)
                self.Email.send({
                    "to"      : client["email"], 
                    "subject" : "Info SELL: current price '{}$'".format(self.current_price),
                    "body"    : ""
                })

    def send_buy_info( self ):
        for client in self.clients:            
            if( int(client["level"]) > 20 and
               float(self.last_price) >= float(client["limitbuy"]) and
               float(self.current_price) < float(client["limitbuy"])
            ):
                print("Info BUY:", client["uid"], client["limitbuy"], self.current_price)                
                self.Email.send({
                    "to"      : client["email"], 
                    "subject" : "Info BUY: current price '{}$'".format(self.current_price),
                    "body"    : ""
                })

# end class SendInfo

si = SendInfo()
si.send_sell_info()
si.send_buy_info()

# end-of-file