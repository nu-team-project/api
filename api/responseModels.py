from pydantic import BaseModel
from typing import Union

class submodel_event_co2(BaseModel):
    ppm:float
    updateTime:str
class model_event_co2(BaseModel):
    co2:submodel_event_co2

class submodel_event_temperature(BaseModel):
    value:float
    updateTime:str
class model_event_temperature(BaseModel):
    temperature:submodel_event_temperature

class submodel_event_batteryStatus(BaseModel):
    percentage:float
    updateTime:str
class model_event_batteryStatus(BaseModel):
    batteryStatus:submodel_event_batteryStatus

class submodel_event_networkStatus(BaseModel):
    signalStrength:int
    rssi:int
    updateTime:str
    cloudConnectors:list
    transmissionMode:str
class model_event_networkStatus(BaseModel):
    networkStatus:submodel_event_networkStatus

class submodel_event_touch(BaseModel):
    updateTime:str
class model_event_touch(BaseModel):
    touch:submodel_event_touch

class submodel_event_humidity(BaseModel):
    temperature:float
    relativeHumidity:float
    updateTime:str
class model_event_humidity(BaseModel):
    humidity:submodel_event_humidity

class submodel_event_ethernetStatus(BaseModel):
    macAddress:str
    ipAddress:str
    errors:list[dict[str,str]]
    updateTime:str
class model_event_ethernetStatus(BaseModel):
    ethernetStatus:submodel_event_ethernetStatus

class submodel_event_cellularStatus(BaseModel):
    signalStrength:float
    errors:list[dict[str,str]]
    updateTime:str
class model_event_cellularStatus(BaseModel):
    cellularStatus:submodel_event_cellularStatus

class submodel_event_connectionStatus(BaseModel):
    connection:str
    available:list[str]
    updateTime:str
class model_event_connectionStatus(BaseModel):
    connectionStatus:submodel_event_connectionStatus

class model_event_list_temperature(BaseModel):
    events: list[Union[
            model_event_temperature,
            model_event_networkStatus,
            model_event_batteryStatus,
            model_event_touch,
        ]]

class model_event_list_humidity(BaseModel):
    events:list[Union[
            model_event_humidity,
            model_event_networkStatus,
            model_event_batteryStatus,
            model_event_touch,
        ]]

class model_event_list_co2(BaseModel):
    events: list[Union[
            model_event_co2,
            model_event_networkStatus,
            model_event_batteryStatus,
            model_event_touch,
        ]]
class model_event_list_ccon(BaseModel):
    events:list[Union[
            model_event_connectionStatus,
            model_event_ethernetStatus,
            model_event_cellularStatus,
            model_event_touch,
        ]]

class model_temperature_events(BaseModel):
    temperature:submodel_event_temperature
    networkStatus:submodel_event_networkStatus
    batteryStatus:submodel_event_batteryStatus
    touch:submodel_event_touch

class model_humidity_events(BaseModel):
    humidity:submodel_event_humidity
    networkStatus:submodel_event_networkStatus
    batteryStatus:submodel_event_batteryStatus
    touch:submodel_event_touch

class model_co2_events(BaseModel):
    co2:submodel_event_co2
    networkStatus:submodel_event_networkStatus
    batteryStatus:submodel_event_batteryStatus
    touch:submodel_event_touch

class model_ccon_events(BaseModel):
    connectionStatus:submodel_event_connectionStatus
    ethernetStatus:submodel_event_ethernetStatus
    cellularStatus:submodel_event_cellularStatus
    touch:submodel_event_touch
    
class model_labels(BaseModel):
    group: Union[str,None]
    show: int

class model_device(BaseModel):
    name: str
    type: str
    labels: model_labels
    events: Union[model_temperature_events,model_humidity_events,model_co2_events,model_ccon_events]
    productNumber: int


class model_device_no_events(BaseModel):
    name: str
    type: str
    labels: model_labels
    productNumber: int

class model_device_empty_events(model_device_no_events):
    events:dict


class model_device_list(BaseModel):
    devices: list[Union[model_device,model_device_empty_events]]

class model_project(BaseModel):
    name:str
    displayName:str
    inventory:bool
    organisation:str
    organisationDisplayName:str
    sensorCount:int
    cloudConnectorCount:int

class model_project_list(BaseModel):
    projects:list[model_project]
    nextPageToken:str


class model_alert(BaseModel):
    alert_id:int
    employee_id:int
    device_name:str
    type:str
    threshold:float
    max:int

class model_alert_list(BaseModel):
    message:str
    alerts:list[model_alert]

class model_alert_create(BaseModel):
    message:str
    newAlert:list[model_alert]

class model_alert_update(BaseModel):
    message:str
    updatedAlert:list[model_alert]

class model_remove(BaseModel):
    message:str


class model_device_create(BaseModel):
    message:str
    newDevice:list[model_device_no_events]

class model_device_update(BaseModel):
    message:str
    updatedDevice:list[model_alert]

class model_error(BaseModel):
    error:str

class model_employee(BaseModel):
    employee_id:int
    username:str
    password:str
    email:str
    first_name:str
    last_name:str

class model_employee_list(BaseModel):
    message:str
    employees:list[model_employee]