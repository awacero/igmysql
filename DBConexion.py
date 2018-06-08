

import sys
HOME="/home/seiscomp/"
LOGFILE="%s/plugins_python/samDB/samDB.log" %HOME
sys.path.append("%s/seiscomp3/share/gds/tools/" %HOME)  


import logging 
logging.basicConfig(filename=LOGFILE,format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)


import MySQLdb



def create_conexionDB(DBHost,port,user,pwd,DBName):
    try:
        conexion=MySQLdb.connect(host=DBHost,user=user,passwd=pwd,port=int(port),db=DBName)
        return conexion
    except Exception as e:
        logging.info("Error in create_ConexionDB(): %s" %str(e))
        return -1


def insert_row(conn,e):
    try:

        query=conn.cursor()
        
        query_str="""INSERT INTO events (eventID,latitude,longitude,description,magVal,magType,timestampSec,timestampNow,depth,status,revision,localizacion,horaLocal)\
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE \
        latitude='%s',longitude='%s',description='%s',magVal='%s',magType='%s',timestampSec='%s',timestampNow='%s',depth='%s',status='%s',revision='%s',localizacion='%s',horaLocal='%s' 
        """ %(e["evid"],e["lat"],e["lon"],e["desc"],e["magVal"],e["magType"],e["timeSec"],e["timeNow"],e["depth"],e["stat"],e["rev"],e["dloc"],e["hloc"],e["lat"],e["lon"],e["desc"],e["magVal"],e["magType"],e["timeSec"],e["timeNow"],e["depth"],e["stat"],e["rev"],e["dloc"],e["hloc"])
        
        #query_str="INSERT INTO gaps_overlaps (estacion,fecha,gaps_d,gaps_c,over_d,over_c) VALUES('%s','%s','%s','%s','%s','%s')" \
        #%(dct['cod'],str(dct['dutc'].datetime),dct['cha_k']['gaps_d'],dct['cha_k']['gaps_c'], dct['cha_k']['over_d'],dct['cha_k']['over_c'] )
        
        logging.info("###QUERY TO TEST:%s" %query_str)

        #'''
        query.execute(query_str)
        conn.commit()
        logging.info("insert_row() OK")
        conn.close()
        #'''
        
    except Exception as ex:
        logging.info("Error in insert_row() %s " %(str(ex)))
        return -1

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


