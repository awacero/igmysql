#!/usr/bin/python
import os

HOME=os.getenv("HOME")
LOGFILE="%s/plugins_python/samDB/delete_samDB.log" %HOME
CONFILE="%s/plugins_python/samDB/send_samDB.cfg" %HOME
import logging 
import ConfigParser 
import json
import DBConexion
logging.basicConfig(filename=LOGFILE,format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)

def readServerFile(json_file):
    try:
        with open(json_file) as json_data_files:
            return json.load(json_data_files)
    except Exception, e:
        logging.info("Error while reading XML _readServerFile()")
       
def deleteEvent(evID,DBname):
    
    config=ConfigParser.ConfigParser()
    config.read(CONFILE)
    json_file=config.get('json','samDBFile')
    
    DB=readServerFile(json_file)
    try:
        db=DB[DBname]
        logging.info("Deleting %s from %s" %(evID,db))
    
    except Exception as e:
        logging.info("Error reading %s in %s : %s" %(DBname,json_file,str(e)))
    
    try:
        dbCon=DBConexion.create_conexionDB(db["host"],db["port"],db["user"],db["pass"],db["DBName"])
        logging.info("DB conexion to %s created" %db)
        logging.info("Delete from DB")
        DBConexion.delete_row(dbCon,evID)
    
    except Exception as e:
        logging.info("Error deleting from DB: %s" %str(e))


#deleteEvent('igepn2018ltil','DEVMYSQL')
      