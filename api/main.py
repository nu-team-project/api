from fastapi import FastAPI, Query
from deviceEmulator import *
from dataFormatter import *
from enum import Enum

Title={
    "app":"Test API with FastAPI"
}
Desc={
"app":"""
# For Team Project and Professionalism
## KV6002
""",
"deviceList":"""
shows generated list of devices, 5 ccons and 25 temp sensors, can be filtered by using the parameter deviceTypes

params in use:

- deviceTypes: list[str]|None=Query(default=None)

unused params:

- deciveIds:list[str]|None=Query(default=None)
- labelFilters:list[str]|None=Query(default=None)
- orderBy:str=None
- query:str=None
- productNumbers:list[str]|None=Query(default=None)
- pageSize:int=None
- pageToken:str=None
""",
"device":"Returns the given projects and device number in an otherwise empty temp sensor JSON object"
}
tags_metadata = [
    {
        "name": "default",
        "description": "The defualt place for new endpoints."
    },
    {
        "name": "Devices & Labels",
        "description": "DS endpoints about devices and labels."
    },
    {
        "name": "Organizations & Projects",
        "description": "DS endpoints about organizations and projects."
    },
    {
        "name": "Not Implemented",
        "description": "These endpoints have not been implemented yet."
    }
]

de=deviceEmulator()
myFormat=dataFormatter()
app = FastAPI(title=Title["app"],description=Desc["app"],openapi_tags=tags_metadata)



@app.get("/",tags=["default"])
async def root():
    return {"message": "Hello, World!"}



@app.get("/projects",tags=["Organizations & Projects"])
async def list_projects(query:str="",pageSize:int=10,pageToken:int=0):
    returnList=de.getProjectList()[pageToken*pageSize:(pageToken+1)*pageSize]
    return {"projects":returnList,"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}",tags=["Not Implemented"],description="NOT CURRENTLY IN USE---PAGE UNDER CONSTRUCTION")
async def get_a_single_project(project):
    return {
        "requested project": project,
        "message": "page under construction"
    }



@app.get("/projects/{project}/devices",tags=["Devices & Labels"],description=Desc["deviceList"])
async def list_sensors_and_cloud_devices(project:str,deciveIds:list[str]|None=Query(default=None),deviceTypes: list[str]|None=Query(default=None),labelFilters:list[str]|None=Query(default=None),orderBy:str=None,query:str=None,productNumbers:list[str]|None=Query(default=None),pageSize:int=None,pageToken:str=None):
        output=[]
        if deviceTypes==None:
            output=de.getDeviceList()
        else:
            if "temperature" in deviceTypes:
                output+=(de.getTempList()) 
            if  "ccon" in deviceTypes:
                output+=(de.getCconList())
        return {"devices":output}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"])
async def get_a_single_device(project:str,device:str,sensorType:str):
    output = myFormat.sensor(project_id=project,device_id=device,sensorType=sensorType,productNumber=0)
    return output