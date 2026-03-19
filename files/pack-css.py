#!/usr/bin/env python

import os, sys, lib.Config
from pathlib import Path

folder = "{}/css".format( lib.Config.Config().config()["static_folder"])
file_list = ["bootstrap.min.css", "bootstrap-icons.css", "master.css"]
ausgabe = ""
dir = Path(folder)
if dir.exists() and dir.is_dir():
    print( "Verzeichnis {} existiert".format(dir) )
    for f in file_list:
        fn = "{}/{}".format( folder, f )
        file = Path( fn )
        if file.exists() and file.is_file():
            print( "  Datei {} existiert".format(fn) )
            eingabe = Path(fn).read_text(encoding="utf-8")
            ausgabe = ausgabe + "\n\n".format(f) + eingabe            
        else: print( "  Datei {} existiert nicht".format(fn) )
        Path( "{}/pack.css".format(folder) ).write_text(ausgabe, encoding="utf-8")
else: print( "Verzeichnis {} existiert nicht".format(dir) )

### end-of-file
