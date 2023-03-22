import random
import string
import datetime
from api.dbConnect import *

class dataRead:
    def __init__(this):
        this.db=dbConnect()

    def getDevices(this,project_id:string=None,deviceTypes:list[str]=None,deviceIds:list[str]=None,labelFilters:list[str]=None):
        if project_id=="i7prjqnb2c4b6rob9xc2":
            sql_where=""
            if deviceTypes is not None:
                if sql_where!="":
                    sql_where+=" AND"
                else:
                    sql_where+=" WHERE"
                sql_where+=" devices.type IN ("
                for i in range(len(deviceTypes)):
                    if i!=0:
                        sql_where+=","
                    sql_where+='"'+deviceTypes[i]+'"'
                sql_where+=")"
            if deviceIds is not None:
                if sql_where!="":
                    sql_where+=" AND"
                else:
                    sql_where+=" WHERE"
                sql_where+=" devices.device_name IN ("
                for i in range(len(deviceIds)):
                    if i!=0:
                        sql_where+=","
                    sql_where+='"'+deviceIds[i]+'"'
                sql_where+=")"
            if labelFilters is not None:
                if sql_where!="":
                    sql_where+=" AND"
                else:
                    sql_where+=" WHERE"
                groups=[]
                show=[]
                for eachLabel in labelFilters:
                    if "=" in eachLabel:
                        splitLabel=eachLabel.split("=")
                        if splitLabel[0]=="group":
                            groups.append(splitLabel[1])    
                        if splitLabel[0]=="show":
                            show.append(splitLabel[1])
                
                if len(groups)>0:
                    sql_where+=" groups.group_name IN ("
                    for i in range(len(groups)):
                        if i!=0:
                            sql_where+=","
                        sql_where+='"'+groups[i]+'"'
                    sql_where+=")"

                if len(show)>0:
                    if len(groups)>0:
                        sql_where+=" AND"
                    sql_where+=" devices.show IN ("
                    for i in range(len(show)):
                        if i!=0:
                            sql_where+=","
                        sql_where+='"'+show[i]+'"'
                    sql_where+=")"
            
            query="""
            SELECT device_name, type, group_name, show, product_number
            FROM devices
            LEFT JOIN groups 
            ON devices.group_id=groups.group_id
            """
            query+=sql_where
            rows=this.db.run_query(query)
            output=[]
            for each in rows:
                output.append({
                    "name":"projects/i7prjqnb2c4b6rob9xc2/devices/"+each[0],
                    "type":each[1],
                    "labels":{
                        "group":each[2],
                        "show":each[3]  
                    },
                    "events":this.__oneDeviceLastEvents(project_id=project_id,device_id=each[0],type=each[1]),
                    "productNumber":each[4]
                })
            return output
            
    def __DT1BetweenDT2andDT3(this,dateTime1:datetime.datetime,dateTime2:datetime.datetime,dateTime3:datetime.datetime):
        if dateTime2<dateTime1 and dateTime1<dateTime3:
            return True
        else:
            return False

    def __oneDeviceLastEvents(this,project_id:str,device_id:str,type:str):
        output={}
        if type == "temperature":
            output["temperature"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["temperature"])[-1]["temperature"]
            output["networkStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["networkStatus"])[-1]["networkStatus"]
            output["batteryStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["batteryStatus"])[-1]["batteryStatus"]
            output["touch"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["touch"])[-1]["touch"]
        elif type == "humidity":
            output["humidity"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["humidity"])[-1]["humidity"]
            output["networkStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["networkStatus"])[-1]["networkStatus"]
            output["batteryStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["batteryStatus"])[-1]["batteryStatus"]
            output["touch"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["touch"])[-1]["touch"]
        elif type == "co2":
            output["co2"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["co2"])[-1]["co2"]
            output["networkStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["networkStatus"])[-1]["networkStatus"]
            output["batteryStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["batteryStatus"])[-1]["batteryStatus"]
            output["touch"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["touch"])[-1]["touch"]
        elif type == "ccon":
            output["connectionStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["connectionStatus"])[-1]["connectionStatus"]
            output["ethernetStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["ethernetStatus"])[-1]["ethernetStatus"]
            output["cellularStatus"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["cellularStatus"])[-1]["cellularStatus"]
            output["touch"]=this.getEvents(project_id=project_id,device_id=device_id,eventTypes=["touch"])[-1]["touch"]
        return output

    def getEvents(this,project_id:string=None,device_id:string=None,eventTypes:list[str]=None,startTime:datetime.datetime=None,endTime:datetime.datetime=None,pageSize:int=None):
        if startTime is None:
            startTime=datetime.datetime.now()-datetime.timedelta(hours = 24)
        if endTime is None:
            endTime=datetime.datetime.now()
        query="""
        SELECT event_id, device_name, value, datetime, event_type
        FROM events
        INNER JOIN devices
        ON events.device_id = devices.device_id
        """
        sql_where='WHERE device_name = "'+device_id+'"'
        if eventTypes is not None:
            sql_where+=" AND events.event_type IN ("
            for i in range(len(eventTypes)):
                if i!=0:
                    sql_where+=","
                sql_where+='"'+eventTypes[i]+'"'
            sql_where+=")"
        query+=sql_where
        rows=this.db.run_query(query)
        output=[]
        for each in rows:
            
            timeFormat="%Y-%m-%dT%H:%M:%S.%fZ"
            if this.__DT1BetweenDT2andDT3(datetime.datetime.strptime(each[3],timeFormat),startTime,endTime):
                if each[4] == "temperature":
                    output.append({
                        "temperature":{
                            "value": each[2],
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "humidity":
                    value=each[2].split(",")
                    temperature=value[0].split(":")[1]
                    relativeHumidity=value[1].split(":")[1]
                    output.append({
                        "humidity":{
                            "temperature": temperature,
                            "relativeHumidity":relativeHumidity,
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "co2":
                    output.append({
                        "co2":{
                            "ppm": each[2],
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "touch":
                    output.append({
                        "touch":{
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "batteryStatus":
                    output.append({
                        "batteryStatus":{
                            "percentage": each[2],
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "networkStatus":
                    value=each[2].split(",")
                    signalStrength=value[0].split(":")[1]
                    rssi=value[1].split(":")[1]
                    cc_id=value[2].split(":")[1]
                    cc_signalStrength=value[3].split(":")[1]
                    cc_rssi=value[4].split(":")[1]
                    transmissionMode=value[5].split(":")[1]
                    output.append({
                        "networkStatus":{
                            "signalStrength": signalStrength,
                            "rssi": rssi,
                            "updateTime": each[3],
                            "cloudConnectors": [{
                                "id": cc_id,
                                "signalStrength": cc_signalStrength,
                                "rssi": cc_rssi,
                            }],
                            "transmissionMode": transmissionMode
                        }
                    })
                elif each[4] == "connectionStatus":
                    value=each[2].split(",")
                    connection=value[0].split(":")[1]
                    available=value[1].split(":")[1].split("[")[1].split("]")[0].split(";")
                    output.append({
                        "connectionStatus": { 
                            "connection": connection,
                            "available": available,
                            "updateTime": each[3]
                        }
                    })
                elif each[4] == "ethernetStatus":
                    value=each[2].split(",")
                    macAddress=value[0].split(":",1)[1]
                    ipAddress=value[1].split(":",1)[1]
                    errors=value[2].split(":",1)[1].split("[")[1].split("]")[0].split(";")
                    errorCode=errors[0].split(":",1)[1]
                    errorMessage=errors[1].split(":",1)[1]
                    output.append({
                        "ethernetStatus": {
                            "macAddress": macAddress,
                            "ipAddress": ipAddress,
                            "errors": [
                                {"code": errorCode, "message": errorMessage},
                            ],
                            "updateTime": each[3],
                        }
                    })
                elif each[4] == "cellularStatus":
                    value=each[2].split(",")
                    signalStrength=value[0].split(":")[1]
                    errors=value[1].split(":",1)[1].split("[")[1].split("]")[0].split(";")
                    errorCode=errors[0].split(":",1)[1]
                    errorMessage=errors[1].split(":",1)[1]
                    output.append({
                        "cellularStatus": {
                            "signalStrength": signalStrength,
                            "errors": [
                                {"code": errorCode, "message": errorMessage},
                            ],
                            "updateTime": each[3],
                        }
                    })
        return output


   
        sql_getAllDevicesAndTypes="""
        SELECT device_id, type
        FROM devices
        WHERE type IN ("temperature", "humidity", "co2", "ccon")
        """
        allDevicesAndTypes=this.db.run_query(sql_getAllDevicesAndTypes)
        for each in allDevicesAndTypes:
            this_device_id=each[0]
            this_device_type=each[1]

            #///////////////////[GET PREVIOUS EVENT VALUES]///////////////////
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
            prev_value={}
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

            #///////////////////[EXTRACT IMPORTANT DATA FROM VALUES]///////////////////
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
                prev_data["networkStatus_signalStrength"]=prev_value["networkStatus"].split(",")[0].split(":")[1]
                prev_data["networkStatus_rssi"]=prev_value["networkStatus"].split(",")[1].split(":")[1]
                prev_data["cellularStatus_signalStrength"]=prev_value["cellularStatus"].split(",")[0].split(":")[1]
            new_data=this.__genEmulatedData(prevData=prev_data,type=this_device_type)

            #///////////////////[WRITE NEW VALUES TO DATABASE]///////////////////
            datetimeFormat="%Y-%m-%dT%H:%M:%S.%fZ"
            datetimeNow=datetime.datetime.strftime(datetime.datetime.now(),datetimeFormat)
            sql_insert="INSERT INTO events (device_id, value, datetime, event_type) VALUES "
            if this_device_type=="temperature":
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["temperature"],datetimeNow,"temperature"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="humidity":
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["humidity"],datetimeNow,"humidity"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="co2":
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["co2"],datetimeNow,"co2"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,new_data["battery"],datetimeNow,"batteryStatus"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["networkStatus"],datetimeNow,"networkStatus"))
            elif this_device_type=="ccon":
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,"-",datetimeNow,"touch"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["ethernetStatus"],datetimeNow,"ethernetStatus"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["connectionStatus"],datetimeNow,"connectionStatus"))
                this.db.run_query(sql_insert+"({},{},{},{})".format(this_device_id,prev_value["cellularStatus"],datetimeNow,"cellularStatus"))
        return

    def __getProjectIdFromName(this,name:str):
        return name.rsplit('/')[2]

    def __getDeviceIdFromName(this,name:str):
        return name.rsplit('/', 1)[-1]

    def __randomString(this,length:int=20):
        return "".join(random.choice(string.ascii_lowercase) for i in range(length))
    
    def __emptyEvents(this,type:str):
        allEvents={
            "sensor":{
                "networkStatus": {
                    "signalStrength": None, #network_signalStrength,
                    "rssi": None, #network_rssi,
                    "updateTime": None, #network_updateTime,
                    "cloudConnectors": [
                        {
                        "id": None, #network_ccon_id,
                        "signalStrength": None, #network_ccon_signalStrength,
                        "rssi": None, #network_ccon_rssi
                        }
                    ],
                    "transmissionMode": "LOW_POWER_STANDARD_MODE"
                },
                "batteryStatus": {
                        "percentage": None, #battery_percentage,
                        "updateTime": None, #battery_updateTime
                },
                "touch": {
                    "updateTime": None, #touch_updateTime
                }
            },
            "ccon":{
                "connectionStatus": {
                    "connection": None, #connStatus_conn, #Either ETHERNET or CELLULAR - ETHERNET if available(see below) or OFFLINE if neither
                    "available": None, #connStatus_available, #["ETHERNET"], ["CELLULAR"], ["ETHERNET","CELLULAR"] or []
                    "updateTime": None #connStatus_updateTime
                },
                "ethernetStatus": {
                    "macAddress": None, #ethernetStatus_macAddress,
                    "ipAddress": None, #ethernetStatus_ipAddress,
                    "errors": [
                        {"code": 404, "message": "Not found"},
                    ],
                    "updateTime": None, #ethernetStatus_updateTime
                },
                "cellularStatus": {
                    "signalStrength": None, #cellularStatus_signalStrength,
                    "errors": [
                        {"code": 404, "message": "Not found"},
                    ],
                    "updateTime": None, #cellularStatus_updateTime
                },
                "touch": {
                    "updateTime": None, #touch_updateTime
                },
            },
            "temperature":{
                "value": None,
                "updateTime": None
            },
            "humidity":{
                "temperature": None,
                "relativeHumidity": None,
                "updateTime": None
            },
            "co2":{
                "co2": {
                    "ppm": None,
                    "updateTime": None
                }
            }
        }
        if type == "ccon":
            events=allEvents["ccon"]
        elif type == "temperature":
            events=allEvents["temperature"]|allEvents["sensor"]
        elif type == "humidity":
            events=allEvents["humidity"]|allEvents["sensor"]
        elif type == "co2":
            events=allEvents["co2"]|allEvents["sensor"]
        else:
            events={}
        return events