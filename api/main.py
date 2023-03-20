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
            ,"--filter projectId":host+"/projects/i7prjqnb2c4b6rob9xc2"
            ,"devices":host+"/projects/i7prjqnb2c4b6rob9xc2/devices"
            ,"--filter sensorTypes":host+"/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature&deviceTypes=co2"
            ,"--filter deviceIds":host+"/projects/i7prjqnb2c4b6rob9xc2/devices?deviceIds=q6xbxrgj42rvjz6bfdgt&deviceIds=k59q5jckmyzm8bpqgb5g"
            ,"device-q6xbxrgj42rvjz6bfdgt":host+"/projects/i7prjqnb2c4b6rob9xc2/devices/q6xbxrgj42rvjz6bfdgt"
        }
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
async def list_sensors_and_cloud_devices(project:str,deviceIds:list[str]|None=Query(default=None),deviceTypes:list[str]|None=Query(default=None),labelFilters:list[str]|None=Query(default=None),orderBy:str=None,query:str=None,productNumbers:list[str]|None=Query(default=None),pageSize:int=None,pageToken:str=None):
    deviceData=myDataRead.getDevices(project_id=project,deviceIds=deviceIds,deviceTypes=deviceTypes,labelFilters=labelFilters)
    return {"devices":deviceData}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"])
async def get_a_single_device(project:str,device:str):
    output = myDataRead.getDevices(project_id=project,deviceIds=[device])
    return output

@app.get("/projects/{project}/devices/{device}/events",tags=["Event History"],description=Desc["eventHistory"])
async def event_history(project:str=None,device:str=None,eventTypes:list[str]=None,startTime:str=None,endTime:str=None,pageSize:int=100):
    print("hello there")
    eventData=myDataRead.getEvents()
    return {"events":eventData}
