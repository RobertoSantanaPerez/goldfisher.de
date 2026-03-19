#!/usr/bin/env python

###############################################################################
#
# Steuerprogramm fuer Clientverwaltung als Konsolenscript auf dem Server
# ----------------------------------------------------------------------
#
# (c) by santana, 2026
#
###############################################################################

import os, sys, argparse, getpass, lib.Client
from sys import argv

parser = argparse.ArgumentParser()
client = lib.Client.Client()

def add_client():
    print("ADD ")
    parser.add_argument("-e", "--email", required=True, help="E-Mail Adresse")
    parser.add_argument("-n", "--name", required=True, help="Name")
    parser.add_argument("-l", "--level", required=True, help="Status")
    args = parser.parse_args()
    param = {
        "uid"    : args.name,
        "email"  : args.email,
        "level"  : args.level,
        "pwd"    : getpass.getpass("please insert password: "),
    }    
    print( "add", param )
    if client.add_client(param): print("done")  
    else: print("fail")  

def del_client():
    print("DEL ")
    parser.add_argument("-n", "--name", required=True, help="Name")
    args = parser.parse_args()
    param = {
        "uid"   : args.name,
    }    
    print("del", param)
    if client.del_client(param): print("done")
    else: print("fail")  

def email_client():
    print("SET EMAIL ")
    parser.add_argument("-n", "--name", required=True, help="Name")
    parser.add_argument("-e", "--email", required=True, help="Name")
    args = parser.parse_args()
    param = {
        "uid"   : args.name,
        "email" : args.email
    }    
    print("set", param)
    if client.email_client(param): print("done")
    else: print("fail")  

def level_client():
    print("SET STATUS ")
    parser.add_argument("-n", "--name", required=True, help="Name")
    parser.add_argument("-l", "--level", required=True, help="Name")
    args = parser.parse_args()
    param = {
        "uid"   : args.name,
        "level" : args.level
    }    
    print("set", param)
    if client.status_client(param): print("done")
    else: print("fail")  

def credit_client():
    print("SET CREDIT ")
    parser.add_argument("-n", "--name", required=True, help="Name")
    parser.add_argument("-c", "--credit", required=True, help="Credit")
    args = parser.parse_args()
    param = {
        "uid"   : args.name,
        "credit" : args.credit
    }    
    print("set", param)
    if client.credit_client(param): print("done")
    else: print("fail")  

action = sys.argv.pop(1)
if action   == "add": add_client()
elif action == "del": del_client()
elif action == "email": email_client()
elif action == "level": level_client()
elif action == "credit": credit_client()
else: print("no Action defined (add/del/email/status/credit)")

# end-of-file

#
# import hashlib
# Text, den du hashen willst
#text = "Hallo Welt"
# MD5-Hash erzeugen
#md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
