#!/usr/bin/env seiscomp-python


import sys,os
sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/'))

from lib import bulletin, spooler
import json
import DBConexion 
import ast

import logging
import logging.config

logging_file = os.path.join(os.environ['SEISCOMP_ROOT'],'var/log/','gds_service_igmysql.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("igmysql")
logger.setLevel(logging.DEBUG)


class samDBConfig:
    def __init__(self,config):
        prefix='json'
        try:
            self.samDBFile=config.get(prefix,"sam_db_credential")
        except:
            logger.info("##There is no sam_db_credential defined")
            self.samDBFile=None

class SpoolSendSamDB(spooler.Spooler):

    def __init__(self):
        logger.info("##CTM llega")
        spooler.Spooler.__init__(self)
        self._conf=samDBConfig(self._config)
        logger.info("##Configuration File Loaded")

    def _readServerFile(self,json_file):
        try:
            with open(json_file) as json_data_files:
                return json.load(json_data_files)
        except Exception as e:
            raise Exception("##Error while reading XML _readServerFile()")       
    
    def spool(self,addresses,content):
        
        logger.info("##Starting spool() for Spool ")

        try:
            b=bulletin.Bulletin()
            b.read(content)
        except Exception as e:
            raise Exception("##Error starting spool(): %s" %(e))

        for a in addresses:

            DBs=self._readServerFile(self._conf.samDBFile)

            try:
                db=DBs[a[1]]
                logger.info("##Storing in DB: %s " %db)
            except Exception as e:
                self.addTargetError(a[0],a[1],(e))
                raise Exception("##Error reading samDB.json: %s" %(e))

            try:
                dbCon=DBConexion.create_conexionDB(db["host"],db["port"],db["user"],db["pass"],db["DBName"]) 
                             
                logger.info("##DB conexion to %s created" %db['DBName'])
                logger.info("##Insert or update in DB")                
                edict=ast.literal_eval(b.plain)
                DBConexion.insert_row(dbCon,edict) 

            except Exception as e:
                
                self.addTargetError(a[0],a[1],(e))
                raise Exception("##Error inserting in DB : %s" %(e))

if __name__=="__main__":
    app=SpoolSendSamDB()
    app()

