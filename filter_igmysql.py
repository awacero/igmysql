#!/usr/bin/env seiscomp-python

import sys,os
sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/')) 


from ig_gds_utilities import ig_utilities as utilities 
from datetime import datetime, timedelta

import seiscomp3.Core
import seiscomp3.DataModel
from lib import bulletin, filter, logger 

import logging
import logging.config

logging_file = os.path.join(os.environ['SEISCOMP_ROOT'],'var/log/','gds_service_igmysql.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("igmysql")
logger.setLevel(logging.DEBUG)


class igmysqlFilter(filter.Filter):
    
    def filter(self,ep):
        
        logging.info("Starting filter for igmysql")
        b=bulletin.Bulletin() 
        e=self.parse_event_parameters(ep)     
        b.plain=str(e)
        return str(b)
        

    def parse_event_parameters(self,ep):
        event={}
        event["id"]= ""
        event["lat"]    = ""
        event["lon"]    = ""
        event["description"] = ""
        event["magVal"] = ""
        event["magType"]=""
        event["timeSec"]= ""
        event["timeNow"]= ""
        event["depth"]  = ""
        event["status"]   = ""
        event["revision"]    = ""
        event["nearest_city"] = ""
        event["local_time"] = ""
        event["type"] = ""
   

        if ep.eventCount()>1:
            return event

        event_object = ep.event(0)
        event["id"] = event_object.publicID()


        for j in range(0,event_object.eventDescriptionCount()):
            ed = event_object.eventDescription(j)
            if ed.type() == seiscomp3.DataModel.REGION_NAME:
                event["description"] = ed.text()
                break

        magnitude = seiscomp3.DataModel.Magnitude.Find(event_object.preferredMagnitudeID())
        if magnitude:
            event['magVal'] = "%0.1f" %magnitude.magnitude().value()
            event["magType"]= magnitude.type()
        origin = seiscomp3.DataModel.Origin.Find(event_object.preferredOriginID())
        if origin:
            event["timeSec"] = origin.time().value().toString("%Y/%m/%d %H:%M:%S")
            event["timeNow"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            local_time=datetime.strptime(event["timeSec"],"%Y/%m/%d %H:%M:%S") -timedelta(hours=5)
            event["local_time"]   = local_time.strftime("%Y/%m/%d %H:%M:%S")
            
            event["lat"]  = "%.4f" % origin.latitude().value() 
            event["lon"]  = "%.4f" % origin.longitude().value()

            try: event["depth"] = "%.4f" % origin.depth().value()
            except seiscomp3.Core.ValueException: event["depth"]="-"
            try: event["status"]  = "%s" %seiscomp3.DataModel.EEvaluationModeNames.name(ep.origin(0).evaluationMode())
            except: event["status"]="NOT SET"
            try:
                typeDescription=event_object.type()
                event["type"] = "%s" %seiscomp3.DataModel.EEventTypeNames.name(typeDescription)
            except: event["type"]="NOT SET"
            
            event['revision']    = '1'
            event['nearest_city']   = utilities.get_closest_city(origin.latitude().value(),origin.longitude().value())
            
        return event


if __name__ == "__main__":
    app = igmysqlFilter()
    sys.exit(app())
