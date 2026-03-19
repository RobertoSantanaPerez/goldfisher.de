#!/usr/bin/env python

from sys import argv
import lib.Config, lib.Shipping, lib.Gold, lib.Variety, lib.ExchangeRate

threshold_for_buy   = 5040
threshold_for_sell  = 5060
smtp_to             = 'roberto@santana-perez.de'
sms_to              = '+4915207870208'

email = lib.Shipping.SMTP()
sms = lib.Shipping.SMS()
gold = lib.Gold.Gold()

sms.ping()
sms.send({
    "to" : "015207870208",
    "body" : "Test SMS"
})

exit()

( current_price, last_price ) = gold.get_current_last_price()
print("{}  {}".format(last_price, current_price))
if( 
    last_price > threshold_for_buy and 
    current_price <= threshold_for_buy
):
    email.send({
        "to" : smtp_to,
        "subject" : "price '{} $' for buy".format( current_price ),
        "body" : ""
    })
    #sms.send({
    #    "to" : sms_to,
    #    "body" : "price '{} $' for buy".format( current_price )
    #})

if( 
    last_price < threshold_for_sell and 
    current_price >= threshold_for_sell 
):
    email.send({
        "to"      : smtp_to,
        "subject" : "price '{} $' for sell".format( current_price ),
        "body"    : ""
    })
    #sms.send({
    #    "to"   : sms_to,
    #    "body" : "price '{} $' for sell".format( current_price )
    #})

# end-of-file

