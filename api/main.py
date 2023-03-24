from typing import Annotated, Union
from fastapi import FastAPI, Query
import httpx
from pydantic import BaseModel
import datetime
from api.dataRead import *
from api.desc import *
from api.emulateData import *
import asyncio

class event(BaseModel):
    event:dict

myDataEmulate=dataEmulater()
myDataRead=dataRead()
app = FastAPI(title=Title["app"],description=Desc["app"],openapi_tags=tags_metadata)


@app.get("/",tags=["default"])
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

@app.get("/test")
async def test():
    return {
        "message":"welcome to the test endpoint"
    }

@app.get("/projects",tags=["Organizations & Projects"],description=Desc["projectList"])
async def list_projects(query:str="",pageSize:int=10,pageToken:int=0):
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
async def list_sensors_and_cloud_devices(project:str,deviceIds:Union[list[str],None]=Query(default=None),deviceTypes:Union[list[str],None]=Query(default=None),labelFilters:Union[list[str],None]=Query(default=None),orderBy:str=None,query:str=None,productNumbers:Union[list[str],None]=Query(default=None),pageSize:int=None,pageToken:str=None):
    deviceData= await myDataRead.getDevices(project_id=project,deviceIds=deviceIds,deviceTypes=deviceTypes,labelFilters=labelFilters)
    return {"devices":deviceData}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"])
async def get_a_single_device(project:str,device:str):
    output = await myDataRead.getDevices(project_id=project,deviceIds=[device])
    return output

@app.get("/projects/{project}/devices/{device}/events",tags=["Event History"],description=Desc["eventHistory"])
async def event_history(project:str,device:str,eventTypes:Union[list[str],None]=Query(default=None),startTime:str=None,endTime:str=None,pageSize:int=100):
    timeFormat="%Y-%m-%dT%H:%M:%S.%fZ"
    if startTime is None:
        startTime=datetime.datetime.now()-datetime.timedelta(hours = 24)
    else:
        startTime=datetime.datetime.strptime(startTime,timeFormat)
    if endTime is None:
        endTime=datetime.datetime.now()
    else:
        endTime=datetime.datetime.strptime(endTime,timeFormat)
    eventData=myDataRead.getEvents(project_id=project,device_id=device,eventTypes=eventTypes,startTime=startTime,endTime=endTime)
    return {"events":eventData}


# {
#   "event": {
#     "id": "emulate",
#     "trigger": "schedule"
#   }
# }

@app.post("/__space/v0/actions")
async def emulate(body:dict):
    # if body["event"]["id"]=="emulate" and body["event"]["trigger"]=="schedule":
    myDataEmulate.emulateData()

@app.get("/emulate")
async def emulate2():
    # if body["event"]["id"]=="emulate" and body["event"]["trigger"]=="schedule":
    myDataEmulate.emulateData()
    return {"message":"emulate"}


@app.get("/esp32")
async def esp32():
    output=await myDataRead.getEspDevice()
    return output