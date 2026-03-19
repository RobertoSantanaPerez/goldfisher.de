#!/usr/bin/env python

from sys import argv
import lib.Gold, lib.Variety, lib.ExchangeRate


try: action = argv[1]
except: action = ""

if action == '-g':
    gold = lib.Gold.Gold()
    gold.insert()
elif action == '-v':
    lib.Variety.Variety().insert()

elif action == '-r':
    rate = lib.ExchangeRate.Rate()
    try: 
        tag = argv[2]
        rate.insert_any_day( tag )
    except: rate.insert_day()
else:
    print("Keine Option angegeben")

# end-of-file
#https://stackoverflow.com/questions/9802102/python-mysql-when-to-explicitly-rollback-a-transaction


