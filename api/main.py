from typing import Union
from fastapi import FastAPI, Query, Path
import datetime
from api.desc import *
from api.dataRead import *
from api.emulateData import *
from api.alertManager import *
from api.deviceManager import *
from api.employeeManager import *
from api.responseModels import *


myDataEmulate=dataEmulater()
myDataRead=dataRead()
myAlerts=alertManager()
myDevices=deviceManager()
myEmployees=employeeManager()
app = FastAPI(title=AppData["title"],description=AppData["desc"],openapi_tags=tags_metadata)


@app.get("/",tags=["Prototype"])
async def root():
    return {
        "message": "Hello, World!"
    }

@app.get("/emulate",tags=["Prototype"],description=Desc["emulate"])
async def emulate():
    myDataEmulate.emulateData()
    return {"message":"success"}

@app.get("/esp32",tags=["Prototype"],description=Desc["esp32"])
async def esp32():
    output=await myDataRead.getEspDevice()
    return output





@app.get("/projects",tags=["Projects"],description=Desc["projectList"],response_model=model_project_list)
async def list_projects():
    return {"projects":[
                {
                    "name":"projects/i7prjqnb2c4b6rob9xc2",
                    "displayName":"Example Project",
                    "inventory":False,
                    "organisation":"organizations/0",
                    "organisationDisplayName": "IoT Monitoring Inc.",
                    "sensorCount":12,
                    "cloudConnectorCount":4
                }
            ],"nextPageToken":"c0un66ecie6seakamrlg"}

@app.get("/projects/{project}",tags=["Projects"],description=Desc["project"],response_model=model_project_list)
async def get_a_single_project(
    project:str=Path(description=QueryDesc["/projects/project"]["project"])
):
    if(project=="i7prjqnb2c4b6rob9xc2"):
        return {"projects":[
                    {
                        "name":"projects/i7prjqnb2c4b6rob9xc2",
                        "displayName":"Example Project",
                        "inventory":False,
                        "organisation":"organizations/0",
                        "organisationDisplayName": "IoT Monitoring Inc.",
                        "sensorCount":12,
                        "cloudConnectorCount":4
                    }
                ],"nextPageToken":"c0un66ecie6seakamrlg"}
    else:
         return {"message":"project not found"}

@app.get("/projects/{project}/devices",tags=["Devices & Labels"],description=Desc["deviceList"],response_model=model_device_list)
async def list_sensors_and_cloud_devices(
    project:str=Path(description=QueryDesc["/projects/project/devices"]["project"]),
    deviceIds:Union[list[str],None]=Query(default=None,description=QueryDesc["/projects/project/devices"]["deviceIds"]),
    deviceTypes:Union[list[str],None]=Query(default=None,description=QueryDesc["/projects/project/devices"]["deviceTypes"]),
    labelFilters:Union[list[str],None]=Query(default=None,description=QueryDesc["/projects/project/devices"]["labelFilters"])
):
    deviceData=await myDataRead.getDevices(project_id=project,deviceIds=deviceIds,deviceTypes=deviceTypes,labelFilters=labelFilters)
    return {"devices":deviceData}

@app.get("/projects/{project}/devices/{device}",tags=["Devices & Labels"],description=Desc["device"],response_model=Union[model_device,model_device_empty_events])
async def get_a_single_device(
    project:str=Path(description=QueryDesc["/projects/project/devices/device"]["project"]),
    device:str=Path(description=QueryDesc["/projects/project/devices/device"]["device"])
):
    output = await myDataRead.getDevices(project_id=project,deviceIds=[device])
    return output[0]

@app.get("/projects/{project}/devices/{device}/events",tags=["Event History"],description=Desc["eventHistory"],response_model=Union[model_event_list_temperature,model_event_list_ccon,model_event_list_humidity,model_event_list_co2])
async def event_history(
    project:str=Path(description=QueryDesc["/projects/project/devices/device/events"]["project"]),
    device:str=Path(description=QueryDesc["/projects/project/devices/device/events"]["device"]),
    eventTypes:Union[list[str],None]=Query(default=None,description=QueryDesc["/projects/project/devices/device/events"]["eventTypes"]),
    startTime:str=Query(default=None,description=QueryDesc["/projects/project/devices/device/events"]["startTime"]),
    endTime:str=Query(default=None,description=QueryDesc["/projects/project/devices/device/events"]["endTime"])
):
    timeFormat="%Y-%m-%dT%H:%M:%SZ"
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






@app.get("/alerts",tags=["Alert Management"],description=Desc["getAlerts"],response_model=Union[model_alert_list,model_error])
async def alerts(
    employee_id:int=Query(default=None,description=QueryDesc["/alerts"]["employee_id"]),
    type:str=Query(default=None,description=QueryDesc["/alerts"]["type"])
): 
    output=myAlerts.getAlerts(employee_id=employee_id,type=type)
    return output

@app.get("/alerts/create",tags=["Alert Management"],description=Desc["createAlerts"],response_model=Union[model_alert_create,model_error])
async def create_alert(
    employee_id:int=Query(description=QueryDesc["/alerts/create"]["employee_id"]),
    device_name:str=Query(description=QueryDesc["/alerts/create"]["device_name"]),
    threshold:float=Query(description=QueryDesc["/alerts/create"]["threshold"]),
    max:int=Query(description=QueryDesc["/alerts/create"]["max"])
): 
    output=myAlerts.createAlerts(employee_id,device_name,threshold,max)
    return output

@app.get("/alerts/update/{alert_id}",tags=["Alert Management"],description=Desc["updateAlerts"],response_model=Union[model_alert_update,model_error])
async def update_alert(
    alert_id:int=Path(description=QueryDesc["/alerts/update/alert_id"]["alert_id"]),
    employee_id:int=Query(default=None,description=QueryDesc["/alerts/update/alert_id"]["employee_id"]),
    device_name:int=Query(default=None,description=QueryDesc["/alerts/update/alert_id"]["device_name"]),
    threshold:float=Query(default=None,description=QueryDesc["/alerts/update/alert_id"]["threshold"]),
    max:int=Query(default=None,description=QueryDesc["/alerts/update/alert_id"]["max"])
): 
    output=myAlerts.updateAlerts(alert_id=alert_id,employee_id=employee_id,device_name=device_name,threshold=threshold,max=max)
    return output

@app.get("/alerts/remove/{alert_id}",tags=["Alert Management"],description=Desc["removeAlerts"],response_model=Union[model_remove,model_error])
async def remove_alert(
    alert_id:int=Path(description=QueryDesc["/alerts/remove/alert_id"]["alert_id"])
): 
    output=myAlerts.removeAlerts(alert_id=alert_id)
    return output


@app.get("/devices/create",tags=["Device Management"],description=Desc["createDevices"],response_model=Union[model_device_create,model_error])
async def create_device(
    device_type:str=Query(description=QueryDesc["/devices/create"]["device_type"]),
    device_name:str=Query(description=QueryDesc["/devices/create"]["device_name"]),
    product_number:int=Query(description=QueryDesc["/devices/create"]["product_number"]),
    show:int=Query(default=1,description=QueryDesc["/devices/create"]["show"]),
    group_name:str=Query(default=None,description=QueryDesc["/devices/create"]["group_name"])
): 
    output=myDevices.createDevice(device_type=device_type,device_name=device_name,product_number=product_number,show=show,group_name=group_name)
    return output

@app.get("/devices/update/{device}",tags=["Device Management"],description=Desc["updateDevices"])
async def update_devices(
    device:str=Path(description=QueryDesc["/devices/update/device"]["device"]),
    device_name:str=Query(default=None,description=QueryDesc["/devices/update/device"]["device_name"]),
    device_type:str=Query(default=None,description=QueryDesc["/devices/update/device"]["device_type"]),
    product_number:int=Query(default=None,description=QueryDesc["/devices/update/device"]["product_number"]),
    show:int=Query(default=None,description=QueryDesc["/devices/update/device"]["show"]),
    group_name:str=Query(default=None,description=QueryDesc["/devices/update/device"]["group_name"])
): 
    device_id=myDevices.getDeviceIDFromName(device_name=device)
    if device_id== {"error":"device_name {} not found".format(device)}:
        return {"error":"unrecognised device {}".format(device)}
    output=myDevices.updateDevice(device_id=device_id["device_id"],device_type=device_type,device_name=device_name,product_number=product_number,show=show,group_name=group_name)
    return output

@app.get("/devices/remove/{device}",tags=["Device Management"],description=Desc["removeDevices"],response_model=Union[model_remove,model_error])
async def remove_device(
    device:str=Path(description=QueryDesc["/devices/remove/device"]["device"])
): 
    output=myDevices.removeDevice(device_name=device)
    return output

@app.get("/employees",tags=["Employee Management"],description=Desc["getEmployees"],response_model=Union[model_employee_list,model_error])
async def get_employees(
    employee_ids:list[int]=Query(default=None,description=QueryDesc["/employees"]["employee_ids"])
):
    output=myEmployees.getEmployees(employee_ids=employee_ids)
    return output