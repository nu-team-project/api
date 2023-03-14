from fastapi import FastAPI, Query

from dataRead import *
from desc import *


myDataRead=dataRead()
app = FastAPI(title=Title["app"],description=Desc["app"],openapi_tags=tags_metadata)


@app.get("/",tags=["default"])
async def root():
    host="http://127.0.0.1:8000"
    return {
        "message": "Hello, World!",
        "links":{
            "docs":host+"/docs"
            ,"projects":host+"/projects/"
            ,"--testingProject":host+"/projects/testing"
            ,"devices":host+"/projects/testing/devices"
            ,"--temperatureSensors":host+"/projects/testing/devices?deviceTypes=temperature"
            ,"--exampleDevice":host+"/projects/testing/devices?deviceIds=example"
            ,"device-exampleDevice":host+"/projects/testing/devices/example"
        }
    }



@app.get("/projects",tags=["Organizations & Projects"],description=Desc["projectList"])
async def list_projects(query:str="",pageSize:int=10,pageToken:int=0):
    return {"projects":[
                {
                    "name":"projects/example",
                    "displayName":"Example Project",
                    "inventory":False,
                    "organisation":"organizations/b8ntihoaplm0028st07g",
                    "organizationDisplayName": "IoT Monitoring Inc.",
                    "sensorCount":6,
                    "cloudConnectorCount":9
                }
            ],"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}",tags=["Not Implemented"],description=Desc["project"])
async def get_a_single_project(project):
    return {
        "requested project": project,
        "message": "page under construction"
    }

@app.get("/projects/{project}/devices",tags=["Devices & Labels"],description=Desc["deviceList"])
async def list_sensors_and_cloud_devices(project:str,deviceIds:list[str]|None=Query(default=None),deviceTypes:list[str]|None=Query(default=None),labelFilters:list[str]|None=Query(default=None),orderBy:str=None,query:str=None,productNumbers:list[str]|None=Query(default=None),pageSize:int=None,pageToken:str=None):
        deviceData=myDataRead.getDevices(project_id=project,deviceIds=deviceIds,deviceTypes=deviceTypes,labelFilters=labelFilters)
        return {"devices":deviceData}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"])
async def get_a_single_device(project:str,device:str,sensorType:str):
    output = myDataRead.getDevices()
    return output
