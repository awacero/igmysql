#!/usr/bin/python
import sys,os
HOME=os.getenv("HOME")
sys.path.append('/%s/seiscomp3/share/gds/tools/' %HOME)

import json
import DBConexion 
import ast

from lib import bulletin, logger, spooler

class samDBConfig:
    def __init__(self,config):
        prefix='json'
        try:
            self.samDBFile=config.get(prefix,"samDBFile")
        except:
            logger.info("##There is no samDBFile Defined")
            self.samDBFile=None

class SpoolSendSamDB(spooler.Spooler):

    def __init__(self):
        spooler.Spooler.__init__(self)
        self._conf=samDBConfig(self._config)
        logger.info("##Configuration File Loaded")

    def _readServerFile(self,json_file):
        try:
            with open(json_file) as json_data_files:
                return json.load(json_data_files)
        except Exception, e:
            raise Exception("##Error while reading XML _readServerFile()")       
    
    def spool(self,addresses,content):
        
        logger.info("##Starting spool() for Spool ")

        try:
            b=bulletin.Bulletin()
            b.read(content)
        except Exception, e:
            raise Exception("##Error starting spool(): %s" %str(e))

        for a in addresses:

            DBs=self._readServerFile(self._conf.samDBFile)

            try:
                db=DBs[a[1]]
                logger.info("##Storing in DB: %s " %db)
            except Exception as e:
                self.addTargetError(a[0],a[1],str(e))
                raise Exception("##Error reading samDB.json: %s" %str(e))

            try:
                dbCon=DBConexion.create_conexionDB(db["host"],db["port"],db["user"],db["pass"],db["DBName"]) 
                             
                logger.info("##DB conexion to %s created" %db['DBName'])
                logger.info("##Insert or update in DB")                
                edict=ast.literal_eval(b.plain)
                DBConexion.insert_row(dbCon,edict) 

            except Exception as e:
                
                self.addTargetError(a[0],a[1],str(e))
                raise Exception("##Error inserting in DB : %s" %str(e))

if __name__=="__main__":
    app=SpoolSendSamDB()
    app()

