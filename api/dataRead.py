import datetime
import httpx
from api.dbConnect import *

class dataRead:
    def __init__(this):
        this.db=dbConnect()
        this.timeFormat="%Y-%m-%dT%H:%M:%SZ"
        this.espTemperatureId="esp32temperature"
        this.espHumidityId="esp32humidity"
        this.espCo2Id="esp32co2"
        this.espLinks={
            "temperature":"https://api.thingspeak.com/channels/2048224/fields/1.json?api_key=WNBPHCR9UFKPAV6N",
            "humidity":"https://api.thingspeak.com/channels/2048224/fields/2.json?api_key=WNBPHCR9UFKPAV6N",
            "co2":"https://api.thingspeak.com/channels/2048224/fields/3.json?api_key=WNBPHCR9UFKPAV6N"
        }

    async def getDevices(this,project_id:str=None,deviceTypes:list[str]=None,deviceIds:list[str]=None,labelFilters:list[str]=None):
        if project_id=="i7prjqnb2c4b6rob9xc2":
            sql_where=""

            # if deviceTypes has values, then add them all to the sql query
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
            
            # if deviceIds has values, then add them all to the sql query
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

            # if labelFilters has values, then add them all to the sql query
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
            
            # get the device data
            query="""
            SELECT device_name, type, group_name, show, product_number
            FROM devices
            LEFT JOIN groups 
            ON devices.group_id=groups.group_id
            """
            query+=sql_where
            rows=this.db.run_query(query)

            # format the data into the Disruptive Technologies format
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
            

            # add the data from the esp32 based devices if applicable
            if labelFilters==None or "group=esp32" in labelFilters:
                esp32jsonFull=await this.getEspDevice()
                esp32List=[]
                if (deviceTypes==None or "temperature" in deviceTypes) and (deviceIds==None or this.espTemperatureId in deviceIds):
                    esp32List.append(esp32jsonFull["temperature"])
                if (deviceTypes==None or "humidity" in deviceTypes) and (deviceIds==None or this.espHumidityId in deviceIds):
                    esp32List.append(esp32jsonFull["humidity"])
                if (deviceTypes==None or "co2" in deviceTypes) and (deviceIds==None or this.espCo2Id in deviceIds):
                    esp32List.append(esp32jsonFull["co2"])
                output=esp32List+output
            return output
            
    def __DT1BetweenDT2andDT3(this,dateTime1:datetime.datetime,dateTime2:datetime.datetime,dateTime3:datetime.datetime):
        # return True if dateTime2<dateTime1<dateTime3
        if dateTime2<dateTime1 and dateTime1<dateTime3:
            return True
        else:
            return False
        
    def __DT1BeforeDT2(this,dateTime1:datetime.datetime,dateTime2:datetime.datetime):
        # return True if dateTime1<dateTime2
        if dateTime2>dateTime1:
            return True
        else:
            return False

    def __oneDeviceLastEvents(this,project_id:str,device_id:str,type:str):
        # get all events associated with the device
        sql_getEvents="""
        SELECT event_id, device_name, value, datetime, event_type
        FROM events
        INNER JOIN devices
        ON events.device_id = devices.device_id
        WHERE device_name = "{}"
        """.format(device_id)
        rows=this.db.run_query(sql_getEvents)
        
        # return nothing if no events found
        if len(rows)==0:
            return {}
        
        # get the most recent events for each device type
        latestEvents={}
        for each in rows:
            each_event_type=each[4]
            if each_event_type in latestEvents.keys():
                if this.__DT1BeforeDT2(datetime.datetime.strptime(latestEvents[each_event_type][3],this.timeFormat),datetime.datetime.strptime(each[3],this.timeFormat)):
                    latestEvents[each_event_type]=each
            else:
                latestEvents[each_event_type]=each
    
        # extract the data for the relavent events based on the device type and format them in the Disruptive Technologies style
        output={}
        if type == "temperature":
            output["temperature"]={"value":latestEvents["temperature"][2],"updateTime":latestEvents["temperature"][3]}
            networkStatus_value=latestEvents["networkStatus"][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": latestEvents["networkStatus"][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": latestEvents["batteryStatus"][2],"updateTime": latestEvents["batteryStatus"][3]} 
            output["touch"]={"updateTime": latestEvents["touch"][3]}
        elif type == "humidity":
            humidity_value=latestEvents["humidity"][2].split(",")
            temperature=humidity_value[0].split(":")[1]
            relativeHumidity=humidity_value[1].split(":")[1]
            output["humidity"]={"temperature": temperature,"relativeHumidity":relativeHumidity,"updateTime":latestEvents["humidity"][3]}
            networkStatus_value=latestEvents["networkStatus"][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": latestEvents["networkStatus"][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": latestEvents["batteryStatus"][2],"updateTime": latestEvents["batteryStatus"][3]}
            output["touch"]={"updateTime": latestEvents["touch"][3]}
        elif type == "co2":
            output["co2"]={"ppm":latestEvents["co2"][2],"updateTime":latestEvents["co2"][3]}    
            networkStatus_value=latestEvents["networkStatus"][2].split(",")
            signalStrength=networkStatus_value[0].split(":")[1]
            rssi=networkStatus_value[1].split(":")[1]
            cc_id=networkStatus_value[2].split(":")[1]
            cc_signalStrength=networkStatus_value[3].split(":")[1]
            cc_rssi=networkStatus_value[4].split(":")[1]
            transmissionMode=networkStatus_value[5].split(":")[1]
            output["networkStatus"]={"signalStrength": signalStrength,"rssi": rssi,"updateTime": latestEvents["networkStatus"][3],"cloudConnectors": [{"id": cc_id,"signalStrength": cc_signalStrength,"rssi": cc_rssi,}],"transmissionMode": transmissionMode}
            output["batteryStatus"]={"percentage": latestEvents["batteryStatus"][2],"updateTime": latestEvents["batteryStatus"][3]}
            output["touch"]={"updateTime": latestEvents["touch"][3]}
        elif type == "ccon":
            connection_value=latestEvents["connectionStatus"][2].split(",")
            connection=connection_value[0].split(":")[1]
            available=connection_value[1].split(":")[1].split("[")[1].split("]")[0].split(";")
            output["connectionStatus"]={ "connection": connection,"available": available,"updateTime": latestEvents["connectionStatus"][3]}
            ethernet_value=latestEvents["ethernetStatus"][2].split(",")
            macAddress=ethernet_value[0].split(":",1)[1]
            ipAddress=ethernet_value[1].split(":",1)[1]
            errors=ethernet_value[2].split(":",1)[1].split("[")[1].split("]")[0].split(";")
            errorCode=errors[0].split(":",1)[1]
            errorMessage=errors[1].split(":",1)[1]
            output["ethernetStatus"]={"macAddress":macAddress,"ipAddress":ipAddress,"errors":[{"code":errorCode,"message":errorMessage},],"updateTime":latestEvents["ethernetStatus"][3]}
            cellular_value=latestEvents["cellularStatus"][2].split(",")
            signalStrength=cellular_value[0].split(":")[1]
            errors=cellular_value[1].split(":",1)[1].split("[")[1].split("]")[0].split(";")
            errorCode=errors[0].split(":",1)[1]
            errorMessage=errors[1].split(":",1)[1]
            output["cellularStatus"]={"signalStrength": signalStrength,"errors":[{"code": errorCode, "message": errorMessage},],"updateTime":latestEvents["cellularStatus"][3],}
            output["touch"]={"updateTime": latestEvents["touch"][3]}
        return output

    async def getEvents(this,project_id:str=None,device_id:str=None,eventTypes:list[str]=None,startTime:datetime.datetime=None,endTime:datetime.datetime=None,pageSize:int=None):
        # set the default values for startTime and endTime
        if startTime is None:
            startTime=datetime.datetime.now()-datetime.timedelta(hours = 24)
        if endTime is None:
            endTime=datetime.datetime.now()

        # add the esp32 based devices to the output if requested
        if device_id in [this.espTemperatureId,this.espHumidityId,this.espCo2Id]:
            datetimeNow=datetime.datetime.strftime(datetime.datetime.now(),this.timeFormat)
            output=[]
            
            if eventTypes==None or "networkStatus" in eventTypes:
                    output.append({
                        "networkStatus": {
                            "signalStrength": "100",
                            "rssi": "0",
                            "updateTime": datetimeNow,
                            "cloudConnectors":[{
                                "id": "esp32",
                                "signalStrength": "100",
                                "rssi": "0"
                            }],
                            "transmissionMode": "LOW_POWER_STANDARD_MODE"
                        }
                    })
            if eventTypes==None or "batteryStatus" in eventTypes:
                    output.append({
                        "batteryStatus": {
                            "percentage": "100",
                            "updateTime": datetimeNow
                        }
                    })
            if eventTypes==None or "touch" in eventTypes:
                    output.append({
                        "touch": {
                            "updateTime": datetimeNow
                        }
                    })
            if device_id==this.espTemperatureId and (eventTypes==None or "temperature" in eventTypes):
                async with httpx.AsyncClient() as client:
                    response = await client.get(this.espLinks["temperature"])
                    esp32feed=response.json()["feeds"]
                reformattedFeed=[]
                for each in esp32feed:
                    reformattedFeed.append({
                        "temperature": {
                            "value": each["field1"],
                            "updateTime": each["created_at"]
                        }
                    })
            elif device_id==this.espHumidityId and (eventTypes==None or "humidity" in eventTypes):
                async with httpx.AsyncClient() as client:
                    response = await client.get(this.espLinks["humidity"])
                    esp32feed=response.json()["feeds"]
                reformattedFeed=[]
                for each in esp32feed:
                    reformattedFeed.append({
                        "humidity": {
                            "temperature": 21,
                            "relativeHumidity": each["field2"],
                            "updateTime": each["created_at"]
                        }
                    })
            elif device_id==this.espCo2Id and (eventTypes==None or "co2" in eventTypes):
                async with httpx.AsyncClient() as client:
                    response = await client.get(this.espLinks["co2"])
                    esp32feed=response.json()["feeds"]
                reformattedFeed=[]
                for each in esp32feed:
                    reformattedFeed.append({
                        "co2": {
                            "ppm": each["field3"],
                            "updateTime": each["created_at"]
                        }
                    })
            output=output+reformattedFeed

        # otherwise return data from the database
        else:
            # get the data for all events in the database
            query="""
            SELECT event_id, device_name, value, datetime, event_type
            FROM events
            INNER JOIN devices
            ON events.device_id = devices.device_id
            """
            sql_where='WHERE device_name = "'+device_id+'"'

            # filter by eventTypes if provided
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

            # for each event retrieved, check the datetime is valid depending on startTime and endTime
            # then format in the Disruptive Technologies style
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
        # get each esp32 based device sensor data seperately and extract the useful data
        async with httpx.AsyncClient() as client:
            response_temp = await client.get(this.espLinks["temperature"])
            response_humidity = await client.get(this.espLinks["humidity"])
            response_co2 = await client.get(this.espLinks["co2"])
            esp32={}
            esp32["temperature"]=response_temp.json()
            esp32["humidity"]=response_humidity.json()
            esp32["co2"]=response_co2.json()
        latest_temperature_event=esp32["temperature"]["feeds"][-1]
        latest_humidity_event=esp32["humidity"]["feeds"][-1]
        latest_co2_event=esp32["co2"]["feeds"][-1]

        # reformat into the Disruptive Technologies style of device data
        datetimeNow=datetime.datetime.strftime(datetime.datetime.now(),this.timeFormat)
        show=1
        esp32Temperature={
            "name": "projects/i7prjqnb2c4b6rob9xc2/devices/"+this.espTemperatureId,
            "type": "temperature",
            "labels": {
                "group": "esp32",
                "show": show
            },
            "events": {
                "temperature": {
                    "value": latest_temperature_event["field1"],
                    "updateTime": latest_temperature_event["created_at"]
                },
                "networkStatus": {"signalStrength": "100","rssi": "0","updateTime": datetimeNow,"cloudConnectors": [{"id": "esp32","signalStrength": "100","rssi": "0"}],"transmissionMode": "LOW_POWER_STANDARD_MODE"},
                "batteryStatus": {"percentage": "100","updateTime": datetimeNow},
                "touch": {"updateTime": datetimeNow}
            },
            "productNumber": esp32["temperature"]["channel"]["id"]+1
        }
        esp32Humidity={
            "name": "projects/i7prjqnb2c4b6rob9xc2/devices/"+this.espHumidityId,
            "type": "humidity",
            "labels": {
                "group": "esp32",
                "show": show
            },
            "events": {
                "humidity": {
                    "temperature": latest_temperature_event["field1"],
                    "relativeHumidity": latest_humidity_event["field2"],
                    "updateTime": latest_humidity_event["created_at"]
                },
                "networkStatus": {"signalStrength": "100","rssi": "0","updateTime": datetimeNow,"cloudConnectors": [{"id": "esp32","signalStrength": "100","rssi": "0"}],"transmissionMode": "LOW_POWER_STANDARD_MODE"},
                "batteryStatus": {"percentage": "100","updateTime": datetimeNow},
                "touch": {"updateTime": datetimeNow}
            },
            "productNumber": esp32["humidity"]["channel"]["id"]+2
        }
        esp32Co2={
            "name": "projects/i7prjqnb2c4b6rob9xc2/devices/"+this.espCo2Id,
            "type": "co2",
            "labels": {
                "group": "esp32",
                "show": show
            },
            "events": {
                "co2": {
                    "ppm": latest_co2_event["field3"],
                    "updateTime": latest_co2_event["created_at"]
                },
                "networkStatus": {"signalStrength": "100","rssi": "0","updateTime": datetimeNow,"cloudConnectors": [{"id": "esp32","signalStrength": "100","rssi": "0"}],"transmissionMode": "LOW_POWER_STANDARD_MODE"},
                "batteryStatus": {"percentage": "100","updateTime": datetimeNow},
                "touch": {"updateTime": datetimeNow}
            },
            "productNumber": esp32["co2"]["channel"]["id"]+3
        }

        # return the data
        result={}
        result["temperature"]=esp32Temperature
        result["humidity"]=esp32Humidity
        result["co2"]=esp32Co2
        return result