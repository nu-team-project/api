from fastapi import FastAPI, Query
from deviceEmulator import *
from dataFormatter import *
from enum import Enum

title="Test API with FastAPI"
description="""
# For Team Project and Professionalism
## KV6002

"""

de=deviceEmulator()
myFormat=dataFormatter()
app = FastAPI(title,description=description)

class Tags(Enum):
    default = "default"
    ds = "Disruptive Systems Endpoints"
    devices="Devices & Labels"
    labels="Devices & Labels"
    none = "Not Implemented"

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/projects")
async def list_projects(query:str="",pageSize:int=10,pageToken:int=0):
    returnList=de.getProjectList()[pageToken*pageSize:(pageToken+1)*pageSize]
    return {"projects":returnList,"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}",tags=[Tags.none],description="NOT CURRENTLY IN USE---PAGE UNDER CONSTRUCTION")
async def get_a_single_project(project):
    return {
        "requested project": project,
        "message": "page under construction"
    }

deviceList_description="""
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
"""
@app.get("/projects/{project}/devices",tags=[Tags.devices],description=deviceList_description)
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

@app.get("/projects/{project}/devices/{device}",description="Returns the given projects and device number in an otherwise empty temp sensor JSON object")
async def get_a_single_device(project:str,device:str):
    productNumber=0
    output = myFormat.temperatureSensor(project,device,productNumber) 
    return output