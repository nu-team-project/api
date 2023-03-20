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