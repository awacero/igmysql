
import sys,os
HOME=os.getenv("HOME")
LOGFILE="%s/plugins_python/samDB/samDB.log" %HOME
sys.path.append("%s/seiscomp3/share/gds/tools/" %HOME)  

import logging 
#logging.basicConfig(filename=LOGFILE,format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)


import MySQLdb

def create_conexionDB(DBHost,port,user,pwd,DBName):
    try:
        conexion=MySQLdb.connect(host=DBHost,user=user,passwd=pwd,port=int(port),db=DBName)
        return conexion
    except Exception as e:
        logging.info("Error in create_ConexionDB(): %s" %str(e))
        raise Exception("Error accessing the server: %s" %str(e))

def insert_row(conn,e):
    try:

        query=conn.cursor()
        
        query_str="""INSERT INTO events (eventID,latitude,longitude,description,magVal,magType,timestampSec,timestampNow,depth,status,revision,localizacion,horaLocal)\
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE \
        latitude='%s',longitude='%s',description='%s',magVal='%s',magType='%s',timestampSec='%s',timestampNow='%s',depth='%s',status='%s',revision='%s',localizacion='%s',horaLocal='%s' 
        """ %(e["id"],e["lat"],e["lon"],e["description"],e["magVal"],e["magType"],e["timeSec"],e["timeNow"],e["depth"],e["status"],e["revision"],e["nearest_city"],e["local_time"],
        e["lat"],e["lon"],e["description"],e["magVal"],e["magType"],e["timeSec"],e["timeNow"],e["depth"],e["status"],e["revision"],e["nearest_city"],e["local_time"])
               
        query.execute(query_str)
        conn.commit()
        logging.info("insert_row() OK")
        conn.close()
        
    except Exception as ex:
        logging.info("Error in insert_row() %s " %(str(ex)))
        raise Exception("Error accessing the server: %s" %str(ex))

def delete_row(conn,evID):
    
    try:
        query=conn.cursor()
        query_str="""DELETE FROM events WHERE eventID='%s'""" %evID
        query.execute(query_str)
        conn.commit()
        logging.info("Deleted event :%s from DB" %evID)
        conn.close()
        
    except Exception as e:
        
        logging.info("##Error in delete_row(): %e" %e)



