#!/usr/bin/python

import sys
HOME="/home/seiscomp/"
LOGFILE="%s/plugins_python/samDB/samDB.log" %HOME
sys.path.append("%s/seiscomp3/share/gds/tools/" %HOME)  


import logging 
logging.basicConfig(filename=LOGFILE,format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)

import distancia 
from datetime import datetime, timedelta

import seiscomp3.Core
import seiscomp3.DataModel
from lib import bulletin, filter, logger 


class samDBFilter(filter.Filter):
    
    def filter(self,ep):
        
        logging.info("Starting filter for samDB")
        b=bulletin.Bulletin() 
        e=self.parseEventParameters(ep)     
        b.plain=str(e)
        return str(b)
        

    def parseEventParameters(self,ep):
        eventDict={}
        eventDict["evid"]= ""
        eventDict["lat"]    = ""
        eventDict["lon"]    = ""
        eventDict["desc"] = ""
        eventDict["magVal"] = ""
        eventDict["magType"]=""
        eventDict["timeSec"]= ""
        eventDict["timeNow"]= ""
        eventDict["depth"]  = ""
        eventDict["stat"]   = ""
        eventDict["rev"]    =""
        eventDict["dloc"]   =""
        eventDict["hloc"]   =""
        eventDict["type"] = ""
   

        if ep.eventCount()>1:
            return eventDict

        event = ep.event(0)
        eventDict["evid"] = event.publicID()


        for j in range(0,event.eventDescriptionCount()):
            ed = event.eventDescription(j)
            if ed.type() == seiscomp3.DataModel.REGION_NAME:
                eventDict["desc"] = ed.text()
                break

        magnitude = seiscomp3.DataModel.Magnitude.Find(event.preferredMagnitudeID())
        if magnitude:
            eventDict['magVal'] = "%0.1f" %magnitude.magnitude().value()
            eventDict["magType"]= magnitude.type()
        origin = seiscomp3.DataModel.Origin.Find(event.preferredOriginID())
        if origin:
            eventDict["timeSec"] = origin.time().value().toString("%Y/%m/%d %H:%M:%S")
            eventDict["timeNow"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            ltime=datetime.strptime(eventDict["timeSec"],"%Y/%m/%d %H:%M:%S") -timedelta(hours=5)
            eventDict["hloc"]   = ltime.strftime("%Y/%m/%d %H:%M:%S")
            
            eventDict["lat"]  = "%.4f" % origin.latitude().value() 
            eventDict["lon"]  = "%.4f" % origin.longitude().value()

            try: eventDict["depth"] = "%.4f" % origin.depth().value()
            except seiscomp3.Core.ValueException: eventDict["depth"]="-"
            try: eventDict["stat"]  = "%s" %seiscomp3.DataModel.EEvaluationModeNames.name(ep.origin(0).evaluationMode())
            except: eventDict["stat"]="NOT SET"
            try:
                typeDescription=event.type()
                eventDict["type"] = "%s" %seiscomp3.DataModel.EEventTypeNames.name(typeDescription)
            except: eventDict["type"]="NOT SET"
            
            eventDict['rev']    = '1'
            eventDict['dloc']   = distancia.closest_distance(origin.latitude().value(),origin.longitude().value())
            
        return eventDict


if __name__ == "__main__":
    app = samDBFilter()
    sys.exit(app())
