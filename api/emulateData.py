import datetime
import random
from api.dbConnect import *

class dataEmulater:
    def __init__(this):
        this.db=dbConnect()
        # Default starting value for events, used if event data is absent from the database
        # This is needed when devices have just been created, and have no events yet
        # Initialising this dictionary here allows easier changing of values during development 
        this.defaultStartValues={
            "temperature":21,
            "humidity":"temperature:21.36,realtiveHumidity:78.59",
            "co2":449,
            "batteryStatus":100,
            "connectionStatus":"connection:ETHERNET,available:[ETHERNET;CELLULAR]",
            "networkStatus":"signalStrength:75,rssi:50,cc_id:rjc3imeidwhx459meiam,cc_signalStrength:70,cc_rssi:25,transmissionMode:LOW_POWER_STANDARD_MODE",
            "touch":0,
            "ethernetStatus":"macAddress:A3:68:12:B4:98:45,ipAddress:192.0.2.1,errors:[code:404;message:not found]",
            "cellularStatus":"signalStrength:70,errors:[code:404;message:not found]",
        }

    def __changeAndRound(this,data:float,maxChangeUp:int,maxChangeDown:int,lowerBound:float,upperBound:float,decimalPlaceChange:int=0,roundTo:int=0) -> float: 
            """
            Make a random change to a float and return the result

            :param float data: The data to operate upon
            :param int maxChangeUp: The maximum increase, in one step in whole numbers
            :param int maxChangeDown: The maximum decrease, in one step in whole numbers
            :param float lowerBound: The lowest number the data can be
            :param float upperBound: The highest number the data can be
            :param int decimalPlaceChange: To how many decimal places can the data be changed default 0
            :param int roundTo: How many decimal places should the data be rounded to after changing default 0
            :return: The changed data
            :rtype: float
            """
            dpcScalar=pow(10,decimalPlaceChange)
            output=data+random.randint(-maxChangeDown*dpcScalar,maxChangeUp*dpcScalar)/(dpcScalar)
            if output<lowerBound:
                output=lowerBound
            elif output>upperBound:
                output=upperBound
            output=round(output,roundTo)
            return output
        
    def __genEmulatedData(this,prevData:dict[str],type:str):
        output={}
        #make changes to the correct types of events for the type of device
        if type=="temperature":
            output["temperature"]=this.__changeAndRound(float(prevData["temperature"]),5,5,12.5,32,1,1)
            if int(float(prevData["battery"]))<=5:
                output["battery"]=100
            else:
                output["battery"]=this.__changeAndRound(float(prevData["battery"]),0,3,5,100)
        elif type=="humidity":
            output["humidity"]=this.__changeAndRound(float(prevData["humidity"]),10,10,10,95,1,1)
            if int(float(prevData["battery"]))<=5:
                output["battery"]=100
            else:
                output["battery"]=this.__changeAndRound(float(prevData["battery"]),0,3,5,100)
        elif type=="co2":
            output["co2"]=this.__changeAndRound(float(prevData["co2"]),25,25,100,300)
            if int(float(prevData["battery"]))<=5:
                output["battery"]=100
            else:
                output["battery"]=this.__changeAndRound(float(prevData["battery"]),0,3,5,100)
        elif type=="ccon":
            #cloud connector information is not generated currently, as it is not needed for the prototype, however this stucture was put in for potential future use
            pass
        return output

    def emulateData(this):
        #get all devices in the database and their types
        sql_getAllDevicesAndTypes="""
        SELECT device_id, type
        FROM devices
        WHERE type IN ("temperature", "humidity", "co2", "ccon")
        """
        allDevicesAndTypes=this.db.run_query(sql_getAllDevicesAndTypes)

        #for each device in the database, get the most recent of each type of event, then store it in the database
        for each in allDevicesAndTypes:
            this_device_id=each[0]
            this_device_type=each[1]
            sql_getLatestEvents="""
            SELECT event_id, device_id, value, datetime, event_type
            FROM (
            SELECT event_id, device_id, value, datetime, event_type
            FROM events
            WHERE device_id = {}
            ORDER BY datetime DESC
            )
            GROUP BY event_type
            """.format(this_device_id)
            latestEvents=this.db.run_query(sql_getLatestEvents)
            
            #go through each event returned and store the values in one dictionary for ease of use.
            prev_value=this.defaultStartValues
            for eachEvent in latestEvents:
                event_type=eachEvent[4]
                event_value=eachEvent[2]
                if event_type == "temperature":
                    prev_value["temperature"]=event_value
                elif event_type == "humidity":
                    prev_value["humidity"]=event_value
                elif event_type == "co2":
                    prev_value["co2"]=event_value
                elif event_type == "batteryStatus":
                    prev_value["batteryStatus"]=event_value
                elif event_type == "connectionStatus":
                    prev_value["connectionStatus"]=event_value
                elif event_type == "networkStatus":
                    prev_value["networkStatus"]=event_value
                elif event_type == "touch":
                    prev_value["touch"]=event_value
                elif event_type == "ethernetStatus":
                    prev_value["ethernetStatus"]=event_value
                elif event_type == "cellularStatus":
                    prev_value["cellularStatus"]=event_value

            #go through the events appropriate to the device and extract the exact data from them that will be operated on
            prev_data={}
            if this_device_type=="temperature":
                prev_data["temperature"]=prev_value["temperature"]
                prev_data["battery"]=prev_value["batteryStatus"]
            elif this_device_type=="humidity":
                prev_data["humidity"]=prev_value["humidity"].split(":")[-1]
                prev_data["battery"]=prev_value["batteryStatus"]
            elif this_device_type=="co2":
                prev_data["co2"]=prev_value["co2"]
                prev_data["battery"]=prev_value["batteryStatus"]
            elif this_device_type=="ccon":
                pass #cloud connector information is not generated currently, as it is not needed for the prototype, however this stucture was put in for potential future use
            
            #generate the new values needed for this device type
            new_data=this.__genEmulatedData(prevData=prev_data,type=this_device_type)

            #write the new events to the database
            datetimeFormat="%Y-%m-%dT%H:%M:%SZ"
            datetimeNow=datetime.datetime.strftime(datetime.datetime.now(),datetimeFormat)
            sql_insert="INSERT INTO events (device_id, value, datetime, event_type) VALUES "
            if this_device_type=="temperature":
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_data["temperature"],datetimeNow,"temperature"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="humidity":
                new_humidity="temperature:21.36,realtiveHumidity:"+str(new_data["humidity"])
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_humidity,datetimeNow,"humidity"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="co2":
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_data["co2"],datetimeNow,"co2"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="ccon":
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["ethernetStatus"],datetimeNow,"ethernetStatus"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["connectionStatus"],datetimeNow,"connectionStatus"))
                this.db.run_no_return(sql_insert+'({},"{}","{}","{}")'.format(this_device_id,prev_value["cellularStatus"],datetimeNow,"cellularStatus"))
        return