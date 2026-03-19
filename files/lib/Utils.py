### begin-of-file

from datetime import date, timedelta
from flask import g, request
import time
import lib.Output

out = lib.Output.Output()

def get_date_today():
  now = time.localtime()
  mon = now.tm_mon if now.tm_mon>10 else "0{}".format(now.tm_mon)
  mday = now.tm_mday if now.tm_mday>10 else "0{}".format(now.tm_mday)
  hour = now.tm_hour if now.tm_hour>10 else "0{}".format(now.tm_hour)
  min = now.tm_min if now.tm_min>10 else "0{}".format(now.tm_min)
  date = "{}-{}-{}".format(
      now.tm_year, mon, mday
  ) 
  return( date )

def get_current_day():
  now = time.localtime()
  mon = now.tm_mon if now.tm_mon>10 else "0{}".format(now.tm_mon)
  mday = now.tm_mday if now.tm_mday>=10 else "0{}".format(now.tm_mday)
  day = "{}-{}-{}".format( now.tm_year, mon, mday )   
  return( day )

def get_current_day_clock():
  now = time.localtime()
  mon = now.tm_mon if now.tm_mon>10 else "0{}".format(now.tm_mon)
  mday = now.tm_mday if now.tm_mday>=10 else "0{}".format(now.tm_mday)
  hour = now.tm_hour if now.tm_hour>=10 else "0{}".format(now.tm_hour)
  min = now.tm_min if now.tm_min>10 else "0{}".format(now.tm_min)
  day = "{}-{}-{}".format( now.tm_year, mon, mday ) 
  clock = "{}:{}:00".format( hour, min )   
  return( day, clock )


def days_from_week(year, week):
    start = date.fromisocalendar(int(year), int(week), 1)    
    days = []
    for i in range(7):
      days.append( str(start + timedelta(days=i)) )
    return( days )

def get_all_clock_for_day():
  list = {}
  for h in range(0,24):
    hour = str(h) if h>9 else  "0{}".format(h)
    for m in range(0, 60):
      min= str(m) if m>9 else  "0{}".format(m)
      stamp = "{}:{}".format(hour, min)
      list[ stamp ] = None
  return( list )

def get_all_clock_for_day_variety():
  list = {}
  for h in range(0,24):
    hour = str(h) if h>9 else  "0{}".format(h)
    for m in range(0, 55, 5):
      min= str(m) if m>9 else  "0{}".format(m)
      stamp = "{}:{}".format(hour, min)
      list[ stamp ] = None
  return( list )

def clock_mysql_program( mysql ):
  clock = str( mysql )
  clock = clock[:-3]
  if len(clock) < 5: 
    clock = "0{}".format(clock)
  return( clock )

def error( str ):
  print( str )
  return( False )

def prediction( list ):
  if len( list ) < 2: return( None )
  last = list[-1]
  count = len(list)  
  summe = 0
  for l in range(count-1, 0, -1):
    summe = summe + list[l] - list[l-1]    
  prediction = float(last)+float(summe/count)  
  return( round(prediction, 2) )
# end prediction

def get_accept():
    accept = request.headers.get("Accept", "")
    if accept == "application/json": return( "application/json" )
    return( "text/html" )
# end get_accept

def error(error):
    if error == 400: errorstr = "Bad Request"
    elif error == 404: errorstr = "File not found"
    else: errorstr = "Unknow Error"
    if "application/json" in lib.Utils.get_accept():
        return( out.json({
            "error"     : error,
            "errorstr"  : errorstr
        }) )
    else:
        g.output["error"]    = error
        g.output["errorstr"] = errorstr
        return( out.html("error") )
  
if __name__ == "__main__":
  pass

### end-of-file