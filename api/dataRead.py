import random
import string

class dataRead:
    def __init__(this):
        this.__deviceList:list[dict]=[]
        this.__numSensors={"temperature":5,"humidity":5,"co2":5}
        this.newDevice(project_id="example",type="ccon",productNumber=9999)
        this.newDevice(project_id="testing",type="ccon",productNumber=1)
        this.newDevice(project_id="testing",type="ccon",device_id="example")

        for type in this.__numSensors.keys():
            for i in range(this.__numSensors[type]):        
                this.newDevice(project_id="testing",type=type)

    def newDevice(this,project_id:str,type:str,device_id:str=None,productNumber:int=None):
        if productNumber is None:
            productNumberList=[]
            for each in this.__deviceList:
                productNumberList.append(each["productNumber"])
            productNumber=max(productNumberList)+1
        if device_id is None:
            deviceIdList=[]
            newId=this.__randomString()
            if len(this.__deviceList) >0:
                for each in this.__deviceList:
                    deviceIdList.append(this.__getDeviceIdFromName(each["name"]))    
                while newId in deviceIdList:
                    newId=this.__randomString()
            device_id=newId
        events=this.__emptyEvents(type)
        thisDevice={
            "name": "/projects/"+project_id+"/devices/"+device_id,
            "type": type,
            "labels": {},
            "reported":events,
            "productNumber": productNumber
        }
        this.__deviceList.append(thisDevice)

    def getDevices(this,project_id:string=None,deviceTypes:list[str]=None,deviceIds:list[str]=None,labelFilters:list[str]=None):
        output=this.__deviceList
        if project_id is not None:
            output=this.__filterDevicesByProjectId(output,project_id)
        if deviceTypes is not None:
            output=this.__filterDevicesByTypes(output,deviceTypes)
        if deviceIds is not None:
            output=this.__filterDevicesByDeviceIds(output,deviceIds)
        if labelFilters is not None:
            output=this.__filterDevicesByLabelFilters(output,labelFilters)
        return output
    
    def __filterDevicesByProjectId(this,deviceList:list[dict],projectId):
        output=[]
        for each in deviceList:
            eachProject=this.__getProjectIdFromName(each["name"])
            if eachProject==projectId:
                output.append(each)
        return output
        
    def __filterDevicesByTypes(this,deviceList:list[dict],types:list[str]):
        output=[]
        for each in deviceList:
            if each["type"] in types:
                output.append(each)
        return output
    
    def __filterDevicesByDeviceIds(this,deviceList:list[dict],deviceIds:list[str]):
        output=[]
        for each in deviceList:
            if this.__getDeviceIdFromName(each["name"]) in deviceIds:
                output.append(each)
        return output
    
    def __filterDevicesByLabelFilters(this,deviceList:list[dict],labelFilters:list[str]):
        output=[]
        for eachDevice in deviceList:#maybe set a new variable as true at start of this loop then set to false if not true, then at end of loop, add to output if true
            for eachLabelFilter in labelFilters:
                if "=" in eachLabelFilter:
                    pass#check if key=value is there
                else:
                    pass#check if key is there
                


        for each in deviceList:
            eachLabels=each["labels"]
            
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