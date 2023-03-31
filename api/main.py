from typing import Annotated, Union
from fastapi import FastAPI, Query
import httpx
from pydantic import BaseModel
import datetime
from api.desc import *
from api.dataRead import *
from api.emulateData import *
from api.alertManager import *
from api.deviceManage import *


myDataEmulate=dataEmulater()
myDataRead=dataRead()
myAlerts=alertManager()
myDevices=deviceManager()
app = FastAPI(title=Title["app"],description=Desc["app"],openapi_tags=tags_metadata)


@app.get("/",tags=["proto"])
async def root():
    host="http://127.0.0.1:8000"
    return {
        "message": "Hello, World!",
        "links":{
            "docs":"/docs"
            ,"projects":"/projects/"
            ,"--filter projectId":"/projects/i7prjqnb2c4b6rob9xc2"
            ,"devices":"/projects/i7prjqnb2c4b6rob9xc2/devices"
            ,"--filter sensorTypes":"/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature&deviceTypes=co2"
            ,"--filter deviceIds":"/projects/i7prjqnb2c4b6rob9xc2/devices?deviceIds=q6xbxrgj42rvjz6bfdgt&deviceIds=k59q5jckmyzm8bpqgb5g"
            ,"--filter labelFilter group":"/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=North%20Wing"
            ,"device-q6xbxrgj42rvjz6bfdgt":"/projects/i7prjqnb2c4b6rob9xc2/devices/q6xbxrgj42rvjz6bfdgt"
        }
    }

@app.get("/test",tags=["proto"])
async def test():
    return {"message":"welcome to the test endpoint"}

@app.get("/emulate",tags=["proto"],description=Desc["emulate"])
async def emulate():
    myDataEmulate.emulateData()
    return {"message":"success"}

@app.get("/esp32",tags=["proto"],description=Desc["esp32"])
async def esp32():
    output=await myDataRead.getEspDevice()
    return output





@app.get("/projects",tags=["Organizations & Projects"],description=Desc["projectList"])
async def list_projects(): #unsused-params: query:str="",pageSize:int=10,pageToken:int=0 
    return {"projects":[
                {
                    "name":"projects/i7prjqnb2c4b6rob9xc2",
                    "displayName":"Example Project",
                    "inventory":False,
                    "organisation":"organizations/0",
                    "organizationDisplayName": "IoT Monitoring Inc.",
                    "sensorCount":12,
                    "cloudConnectorCount":4
                }
            ],"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}",tags=["Organizations & Projects"],description=Desc["project"])
async def get_a_single_project(project):
    if(project=="i7prjqnb2c4b6rob9xc2"):
        return {"projects":[
                    {
                        "name":"projects/i7prjqnb2c4b6rob9xc2",
                        "displayName":"Example Project",
                        "inventory":False,
                        "organisation":"organizations/0",
                        "organizationDisplayName": "IoT Monitoring Inc.",
                        "sensorCount":12,
                        "cloudConnectorCount":4
                    }
                ],"nextPageToken":"c0un66ecie6seakamrlg"}
    else:
         return {"message":"project not found"}

@app.get("/projects/{project}/devices",tags=["Devices & Labels"],description=Desc["deviceList"])
async def list_sensors_and_cloud_devices(project:str,deviceIds:Union[list[str],None]=Query(default=None),deviceTypes:Union[list[str],None]=Query(default=None),labelFilters:Union[list[str],None]=Query(default=None)): #unused-params: orderBy:str=None,query:str=None,productNumbers:Union[list[str],None]=Query(default=None),pageSize:int=None,pageToken:str=None
    deviceData= await myDataRead.getDevices(project_id=project,deviceIds=deviceIds,deviceTypes=deviceTypes,labelFilters=labelFilters)
    return {"devices":deviceData}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"])
async def get_a_single_device(project:str,device:str):
    output = await myDataRead.getDevices(project_id=project,deviceIds=[device])
    return output

@app.get("/projects/{project}/devices/{device}/events",tags=["Event History"],description=Desc["eventHistory"])
async def event_history(project:str,device:str,eventTypes:Union[list[str],None]=Query(default=None),startTime:str=None,endTime:str=None): #unused-params: pageSize:int=100
    timeFormat="%Y-%m-%dT%H:%M:%S.%fZ"
    if startTime is None:
        startTime=datetime.datetime.now()-datetime.timedelta(hours = 24)
    else:
        startTime=datetime.datetime.strptime(startTime,timeFormat)
    if endTime is None:
        endTime=datetime.datetime.now()
    else:
        endTime=datetime.datetime.strptime(endTime,timeFormat)
    eventData=await myDataRead.getEvents(project_id=project,device_id=device,eventTypes=eventTypes,startTime=startTime,endTime=endTime)
    return {"events":eventData}






@app.get("/alerts",tags=["Custom"],description=Desc["getAlerts"]) #this will require auth eventually
async def alerts(employee_id:int=None,type:str=None,event_id:int=None): 
    output=myAlerts.getAlerts(employee_id=employee_id,type=type,event_id=event_id)
    return output

@app.get("/alerts/create",tags=["Custom"],description=Desc["createAlerts"]) #this will require auth eventually
async def create_alert(employee_id:int,device_name:str,threshold:float,max:int): 
    output=myAlerts.createAlerts(employee_id,device_name,threshold,max)
    return output

@app.get("/alerts/update/{alert_id}",tags=["Custom"],description=Desc["updateAlerts"]) #this will require auth eventually
async def update_alert(alert_id:int,employee_id:int=None,device_id:int=None,threshold:float=None,max:int=None): 
    output=myAlerts.updateAlerts(alert_id=alert_id,employee_id=employee_id,device_id=device_id,threshold=threshold,max=max)
    return output

@app.get("/alerts/remove/{alert_id}",tags=["Custom"],description=Desc["removeAlerts"]) #this will require auth eventually
async def remove_alert(alert_id:int): 
    output=myAlerts.removeAlerts(alert_id=alert_id)
    return output


@app.get("/devices/create",tags=["Custom"],description=Desc["createDevices"]) #this will require auth eventually
async def create_device(device_type:str,device_name:str,product_number:int,show:int=1,group_name:str=None): 
    output=myDevices.createDevice(device_type=device_type,device_name=device_name,product_number=product_number,show=show,group_name=group_name)
    return output
    

@app.get("/devices/update/{device_id}",tags=["Custom"],description=Desc["updateDevices"]) #this will require auth eventually
async def update_devices(device_id:str,device_name:str=None,device_type:str=None,product_number:int=None,show:int=None,group_name:str=None): 
    output=myDevices.updateDevice(device_id=device_id,device_type=device_type,device_name=device_name,product_number=product_number,show=show,group_name=group_name)
    return output

@app.get("/devices/remove/{device}",tags=["Custom"],description=Desc["removeDevices"]) #this will require auth eventually
async def remove_device(device_id:int): 
    output=myDevices.removeDevice(device_id=device_id)
    return output