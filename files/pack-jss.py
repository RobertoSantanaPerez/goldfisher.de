#!/usr/bin/env python

import os, sys, lib.Config
from pathlib import Path

ausgabe     = ""
folder      = "{}/jss".format( lib.Config.Config().config()["static_folder"])
file_list   = [
    "bootstrap.bundle.min.js",  "flatpickr.min.js", "sprintf.min.js", 
    "plotly.min.js", "ajv.bundle.js", "htmx.min.js", "master.js", 
]

node_module_files = []

project_root = Path(__file__).resolve().parents[1]

dir = Path(folder)
if dir.exists() and dir.is_dir():
    print( "Verzeichnis {} existiert".format(dir) )
    for f in file_list:
        fn = "{}/{}".format( folder, f )
        file = Path( fn )
        if file.exists() and file.is_file():
            print( "  Datei {} existiert".format(fn) )
            eingabe = Path(fn).read_text(encoding="utf-8")
            ausgabe = ausgabe + "\n/* {} */\n".format(f) + eingabe            
        else:
            print( "  Datei {} existiert nicht".format(fn) )

    # include node_modules files
    for rel in node_module_files:
        nmf = project_root / "node_modules" / rel
        chosen = None
        if nmf.exists() and nmf.is_file():
            chosen = nmf
        else:
            try:
                fallback = nmf.with_name(nmf.name.replace('.min', ''))
            except Exception:
                fallback = None
            if fallback and fallback.exists() and fallback.is_file():
                chosen = fallback

        if chosen:
            print("  Node-Modul-Datei {} existiert".format(chosen))
            eingabe = chosen.read_text(encoding="utf-8")
            ausgabe += "\n/* node_modules/{} */\n".format(rel) + eingabe
        else:
            print("  Node-Modul-Datei {} existiert nicht".format(nmf))

    Path( "{}/pack.js".format(folder) ).write_text(ausgabe, encoding="utf-8")
else:
    print( "Verzeichnis {} existiert nicht".format(dir) )

### end-of-file
