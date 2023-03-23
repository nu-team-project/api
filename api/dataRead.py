import random
import string
import datetime
from api.dbConnect import *
import httpx
import asyncio

class dataRead:
    def __init__(this):
        this.db=dbConnect()
        this.timeFormat="%Y-%m-%dT%H:%M:%S.%fZ"

    async def getDevices(this,project_id:string=None,deviceTypes:list[str]=None,deviceIds:list[str]=None,labelFilters:list[str]=None):
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
            
            if labelFilters==None or "esp32" in labelFilters:
                esp32jsonFull= await this.getEspDevice()
                esp32List=[]
                if deviceTypes==None or "temperature" in deviceTypes:
                    esp32List.append(esp32jsonFull["temperature"])
                if deviceTypes==None or "humidity" in deviceTypes:
                    esp32List.append(esp32jsonFull["humidity"])
                if deviceTypes==None or "co2" in deviceTypes:
                    esp32List.append(esp32jsonFull["co2"])
                output=esp32List+output

            return output
            
    def __DT1BetweenDT2andDT3(this,dateTime1:datetime.datetime,dateTime2:datetime.datetime,dateTime3:datetime.datetime):
        if dateTime2<dateTime1 and dateTime1<dateTime3:
            return True
        else:
            return False

    def __oneDeviceLastEvents(this,project_id:str,device_id:str,type:str):
        sql_latestEvents="""
        SELECT event_id, device_name, value, datetime, event_type
        FROM (
        SELECT event_id, device_name, value, datetime, event_type
        FROM events
        INNER JOIN devices
        ON events.device_id = devices.device_id
        WHERE device_name = "{}"
        ORDER BY datetime DESC
        )
        GROUP BY event_type
        ORDER BY event_type
        """.format(device_id)
        rows=this.db.run_query(sql_latestEvents)
        output={}
        if type == "temperature":
            output["temperature"]={"value":rows[2][2],"updateTime":rows[2][3]}
            networkStatus_value=rows[1][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": rows[1][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": rows[0][2],"updateTime": rows[0][3]} 
            output["touch"]={"updateTime": rows[3][3]}
        elif type == "humidity":
            humidity_value=rows[1][2].split(",")
            temperature=humidity_value[0].split(":")[1]
            relativeHumidity=humidity_value[1].split(":")[1]
            output["humidity"]={"temperature": temperature,"relativeHumidity":relativeHumidity,"updateTime":rows[1][3]}
            networkStatus_value=rows[2][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": rows[2][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": rows[0][2],"updateTime": rows[0][3]}
            output["touch"]={"updateTime": rows[3][3]}
        elif type == "co2":
            output["co2"]={"ppm":rows[1][2],"updateTime":rows[1][3]}    
            networkStatus_value=rows[2][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": rows[2][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": rows[0][2],"updateTime": rows[0][3]}
            output["touch"]={"updateTime": rows[3][3]}
        elif type == "ccon":
            connection_value=rows[1][2].split(",")
            connection=connection_value[0].split(":")[1]
            available=connection_value[1].split(":")[1].split("[")[1].split("]")[0].split(";")
            output["connectionStatus"]={ "connection": connection,"available": available,"updateTime": rows[1][3]}
            ethernet_value=rows[2][2].split(",")
            macAddress=ethernet_value[0].split(":",1)[1]
            ipAddress=ethernet_value[1].split(":",1)[1]
            errors=ethernet_value[2].split(":",1)[1].split("[")[1].split("]")[0].split(";")
            errorCode=errors[0].split(":",1)[1]
            errorMessage=errors[1].split(":",1)[1]
            output["ethernetStatus"]={"macAddress":macAddress,"ipAddress":ipAddress,"errors":[{"code":errorCode,"message":errorMessage},],"updateTime":rows[2][3]}
            cellular_value=rows[0][2].split(",")
            signalStrength=cellular_value[0].split(":")[1]
            errors=cellular_value[1].split(":",1)[1].split("[")[1].split("]")[0].split(";")
            errorCode=errors[0].split(":",1)[1]
            errorMessage=errors[1].split(":",1)[1]
            output["cellularStatus"]={"signalStrength": signalStrength,"errors":[{"code": errorCode, "message": errorMessage},],"updateTime":rows[0][3],}
            output["touch"]={"updateTime": rows[3][3]}
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
            if this.__DT1BetweenDT2andDT3(datetime.datetime.strptime(each[3],this.timeFormat),startTime,endTime):
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

    async def getEspDevice(this):
        link="https://api.thingspeak.com/channels/2048224/fields/1.json?api_key=WNBPHCR9UFKPAV6N&results=2"
        async with httpx.AsyncClient() as client:
            response = await client.get(link)
            esp32=response.json()
        # {
        #     "channel":{
        #         "id":2048224,
        #         "name":"esp32",
        #         "latitude":"0.0",
        #         "longitude":"0.0",
        #         "field1":"temp",
        #         "field2":"humidity",
        #         "field3":"eco2",
        #         "created_at":"2023-02-28T09:45:47Z",
        #         "updated_at":"2023-03-16T03:18:15Z",
        #         "last_entry_id":1078
        #     },
        #     "feeds":[
        #         {
        #             "created_at":"2023-03-16T12:21:41Z",
        #             "entry_id":1077,
        #             "field1":"25.27561"
        #         },
        #         {
        #             "created_at":"2023-03-16T12:22:12Z",
        #             "entry_id":1078,
        #             "field1":"25.29774"
        #         }
        #     ]
        # }
        latest_event=esp32["feeds"][-1]
        datetimeNow=datetime.datetime.strftime(datetime.datetime.now(),this.timeFormat)
        show=1
        esp32Temperature={
            "name": "projects/i7prjqnb2c4b6rob9xc2/devices/esp32temperature",
            "type": "temperature",
            "labels": {
                "group": "esp32",
                "show": show
            },
            "events": {
                "temperature": {
                    "value": latest_event["field1"],
                    "updateTime": latest_event["created_at"]
                },
                "networkStatus": {
                    "signalStrength": "100",
                    "rssi": "0",
                    "updateTime": datetimeNow,
                    "cloudConnectors": [
                    {
                        "id": "esp32",
                        "signalStrength": "100",
                        "rssi": "0"
                    }
                    ],
                    "transmissionMode": "LOW_POWER_STANDARD_MODE"
                },
                "batteryStatus": {
                    "percentage": "100",
                    "updateTime": datetimeNow
                },
                "touch": {
                    "updateTime": datetimeNow
                }
            },
            "productNumber": esp32["channel"]["id"]
        }
        result={}
        result["temperature"]=esp32Temperature
        result["humidity"]={"name": "projects/i7prjqnb2c4b6rob9xc2/devices/esp32humidity"}
        result["co2"]={"name": "projects/i7prjqnb2c4b6rob9xc2/devices/esp32co2"}
        return result

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