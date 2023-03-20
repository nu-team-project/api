import random
import string
from dbConnect import *

class dataRead:
    def __init__(this):
        this.db=dbConnect()

    def getDevices(this,project_id:string=None,deviceTypes:list[str]=None,deviceIds:list[str]=None,labelFilters:list[str]=None):
        if project_id=="i7prjqnb2c4b6rob9xc2":
            sql_where=""
            if deviceTypes is not None:
                if sql_where!="":
                    sql_where+=" AND"
                sql_where+=" WHERE devices.type IN ("
                for i in range(len(deviceTypes)):
                    if i!=0:
                        sql_where+=","
                    sql_where+='"'+deviceTypes[i]+'"'
                sql_where+=")"
            if deviceIds is not None:
                if sql_where!="":
                    sql_where+=" AND"
                sql_where+=" WHERE devices.device_name IN ("
                for i in range(len(deviceIds)):
                    if i!=0:
                        sql_where+=","
                    sql_where+='"'+deviceIds[i]+'"'
                sql_where+=")"
            if labelFilters is not None:
                if sql_where!="":
                    sql_where+=" AND"
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
                    sql_where+=" WHERE groups.group_name IN ("
                    for i in range(len(groups)):
                        if i!=0:
                            sql_where+=","
                        sql_where+='"'+groups[i]+'"'
                    sql_where+=")"

                if len(show)>0:
                    sql_where+=" WHERE devices.show IN ("
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
            print("Query = "+query)
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
                    "events":this.__emptyEvents(each[1]),
                    "productNumber":each[4]
                })
            return output
    
    def getEvents(this):
        print("hello")
        query="""
        SELECT event_id, device_id, value, datetime, event_type
        FROM events
        """
        print("Query = "+query)
        rows=this.db.run_query(query)
        output=[]
        for each in rows:
            output.append({
                "event_id":each[0], #remove
                "device_id":each[1] #remove
            })
            match each[4]:
                
                
                case "temperature":
                    output.append({
                        "temperature":{
                            "value": each[2],
                            "updateTime": each[3]
                        }
                    })
                case "humidity":
                    output.append({
                        "humidity":{
                            "value": each[2], #needs to split temp and relative humidity
                            "updateTime": each[3]
                        }
                    })
                case "co2":
                    output.append({
                        "co2":{
                            "ppm": each[2],
                            "updateTime": each[3]
                        }
                    })
                case "touch":
                    output.append({
                        "touch":{
                            "updateTime": each[3]
                        }
                    })
                case "battery":
                    output.append({
                        "batteryStatus":{
                            "percentage": each[2],
                            "updateTime": each[3]
                        }
                    })
                case "network":
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
                case "connStatus":
                    value=each[2].split(",")
                    connection=value[0].split(":")[1]
                    available=value[1].split(":")[1]
                    output.append({
                        "connectionStatus": { 
                            "connection": connection,
                            "available": available,
                            "updateTime": each[3]
                        }
                    })
                case "etherStatus":
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
                case "cellStatus":
                    value=each[2].split(",") #signalStrength:70,errors:[code:404,message:not found]
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
        match type:
            case "ccon":
                events=allEvents["ccon"]
            case "temperature":
                events=allEvents["temperature"]|allEvents["sensor"]
            case "humidity":
                events=allEvents["humidity"]|allEvents["sensor"]
            case "co2":
                events=allEvents["co2"]|allEvents["sensor"]
            case _:
                events={}
        return events