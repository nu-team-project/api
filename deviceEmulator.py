import random
import string

class deviceEmulator:
    def __init__(this):
        this.projectList=this.__genProjectList()
        this.cconList=this.__genCconList(this.projectList)
        this.tempList=this.__genTempList(this.projectList,this.cconList)

    def getProjectList(this):
        return this.projectList
    
    def getDeviceList(this):
        return this.cconList+this.tempList
    
    def getCconList(this):
        return this.cconList
    
    def getTempList(this):
        return this.tempList

    def __genProjectList(this,numberOfProjects=1):
        projectList=[{
                "name":"projects/example",
                "displayName":"Example Project",
                "inventory":False,
                "organisation":"organizations/b8ntihoaplm0028st07g",
                "organizationDisplayName": "IoT Monitoring Inc.",
                "sensorCount":6,
                "cloudConnectorCount":9
            }]
        while len(projectList)<=numberOfProjects:
            project_id = len(projectList)+1
            project = {
                "name":"projects/"+("".join(random.choice(string.ascii_lowercase) for i in range(20))),
                "displayName":"Project {}".format(project_id),
                "inventory":False,
                "organisation":"organizations/b8ntihoaplm0028st07g",
                "organizationDisplayName": "IoT Monitoring Inc.",
                "sensorCount": random.randint(1,20),
                "cloudConnectorCount": random.randint(1,10)
            }
            projectList.append(project)
        return projectList
    
    def __genCconList(this,thisProjectList,numCcon=5):
        thisProject=thisProjectList[0]["name"]
        cconList=[]
        while len(cconList)<numCcon:
            device_id="".join(random.choice(string.ascii_lowercase) for i in range(20))
            signalStrength=random.randint(25,90)
            updateTime="2021-03-03T08:04:30.373046Z"
            productNumber="102058"
            possible_available=[["CELLULAR","ETHERNET"],["CELLULAR"],["ETHERNET"]]
            available=possible_available[random.randint(0,2)]
            connection="CELLULAR" if available == ["CELLULAR"] else "ETHERNET"
            macAddress="f0:b5:b7:00:0a:08"
            ipAddress="10.0.0.1"
            cconList.append(
                {
                    "name": thisProject+"/devices/"+device_id,
                    "type": "ccon",
                    "labels": {},
                    "reported": {        
                        "connectionStatus": {
                            "connection": connection,
                            "available": available,
                            "updateTime": updateTime
                        },
                        "ethernetStatus": {
                            "macAddress": macAddress,
                            "ipAddress": ipAddress,
                            "errors": [
                                {"code": 404, "message": "Not found"},
                            ],
                            "updateTime": updateTime
                        },
                        "cellularStatus": {
                            "signalStrength": signalStrength,
                            "errors": [
                                {"code": 404, "message": "Not found"},
                            ],
                            "updateTime": updateTime
                        },
                        "touch": {
                            "updateTime": updateTime
                        }                
                    },
                    "productNumber": productNumber
                }
            )
        return cconList

    def __genTempList(this,thisProjectList,cconList,numTemp=25):
        thisProject=thisProjectList[0]["name"]
        tempList=[]
        while len(tempList)<numTemp:
            device_id="".join(random.choice(string.ascii_lowercase) for i in range(20))
            signalStrength=random.randint(25,90)
            ccon_id=cconList[random.randint(0,len(cconList)-1)]["name"].rsplit('/', 1)[-1]
            rssi=-random.randint(70,100)
            updateTime="2021-03-03T08:04:30.373046Z"
            productNumber="102058"
            temperature=random.randint(5,40)
            batteryPercentage=random.randint(25,100)
            tempList.append(
                {
                    "name": thisProject+"/devices/"+device_id,
                    "type": "temperature",
                    "labels": {},
                    "reported": {
                        "networkStatus": {
                            "signalStrength": signalStrength,
                            "rssi": rssi,
                            "updateTime": updateTime,
                            "cloudConnectors": [
                                {
                                "id": ccon_id,
                                "signalStrength": signalStrength,
                                "rssi": rssi
                                }
                            ],
                            "transmissionMode": "LOW_POWER_STANDARD_MODE"
                        },
                        "batteryStatus": {
                            "percentage": batteryPercentage,
                            "updateTime": updateTime
                        },
                        "temperature": {
                        "value": temperature,
                        "updateTime": updateTime
                        }
                    },
                    "productNumber": productNumber
                }
            )
        return tempList
