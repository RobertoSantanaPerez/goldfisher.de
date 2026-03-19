import time, json, requests
import lib.MySQL, lib.Utils

class Info( lib.MySQL.Mysql ):

    def __init__( self ):
        super().__init__()        
        pass
    
    def get_info_list( self ):
        list = []
        self.cursor.execute(
            "SELECT id, title, url, day, clock FROM info"
        )
        rows = self.cursor.fetchall()    
        for row in rows:          
            list.append({
                "id"    : str(row[0]),
                "title" : str(row[1]),
                "url"   : str(row[2]),
                "day"   : str(row[3]),
                "clock" : str(row[4])
            })            
        self.cursor.close()
        return( list )
    # get_info_list

    def delete( self, id ):
        try:
            self.transaction()
            self.cursor.execute(
                "DELETE FROM infocontent WHERE info_id=%s",
                [ id ]
            )
            self.cursor.execute(
                "DELETE FROM info WHERE id=%s",
                [ id ]
            )
            self.commit()
            return( True )
        except: pass
        return( False )
    # end delete

    def get_info( self, id ):
        self.cursor.execute(
            "SELECT i.id, i.day, i.clock, i.title, i.url, ic.comment, ic.content, ic.pdf" 
            + " FROM info i, infocontent ic WHERE i.id=%s AND i.id=ic.info_id",
            [ id ]
        )
        try:        
            id,day,clock,title,url,comment,content,pdf, = self.cursor.fetchone()
            return({
                "id"        : id,
                "day"       : day,
                "clock"     : clock,
                "title"     : title,
                "url"       : url ,
                "comment"   : comment,
                "content"   : content,
                "pdf"       : pdf,
            })
        except: pass
        return( None )

    def insert( self, data ):
        ( day, clock ) = lib.Utils.get_current_day_clock() 
        try:
            self.transaction()
            self.cursor.execute(
                "INSERT INTO info SET day=%s, clock=%s, title=%s, url=%s",
                [ day, clock, data["title"], data["url"] ]
            ) 
            last_info_id = self.cursor.lastrowid     
            self.cursor.execute(
                "INSERT INTO infocontent SET info_id=%s, comment=%s, content=%s, pdf=%s",
                [ last_info_id, data["comment"], data["content"], data["pdf"] ]
            )
            self.commit()
            return( last_info_id )
        except: pass
        return( None )
    
    def update( self, data ):
        try:
            self.transaction()
            self.cursor.execute(
                "UPDATE info SET title=%s, url=%s WHERE id=%s",
                [ data["title"], data["url"], data["id"] ]
            ) 
            self.cursor.execute(
                "UPDATE infocontent SET comment=%s, content=%s, pdf=%s WHERE info_id=%s",
                [ data["comment"], data["content"], data["pdf"], data["id"] ]
            )
            self.commit()
            return( True )
        except: pass
        return( None )
    
# end-of-file
