from fastapi import FastAPI, Query
from deviceEmulator import *
from enum import Enum


descripion="""
# For Team Project and Professionalism
## KV6002
"""


de=deviceEmulator()
app = FastAPI(title="Test API with FastAPI",description=descripion)

class Tags(Enum):
    test = "test"
    ds = "ds endpoints"



@app.get("/", tags=[Tags.test])
async def root():
    return {"message": "Hello, World!"}

@app.get("/greet", tags=[Tags.test])
async def hello(name:str="Everyone",greeting:str="Hello"):
    return {"message": "{}, {}!".format(greeting,name)}

@app.get("/list", tags=[Tags.test])
@app.get("/list/{num}", tags=[Tags.test])
async def list_devices(num:int=4):
    list=[]
    a=0
    while a<num:
        list.append({"name":"Device {}".format(a+1),"tag":"Tag {}".format(a+1)})
        a+=1
    return {"message":list}



@app.get("/projects", tags=[Tags.ds])
async def list_projects(query:str="",pageSize:int=10,pageToken:int=0):
    returnList=de.getProjectList()[pageToken*pageSize:(pageToken+1)*pageSize]
    return {"projects":returnList,"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}/devices", tags=[Tags.ds])
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