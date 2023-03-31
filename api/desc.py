Title={
    "app":"Test API with FastAPI"
}
Desc={
"app":"""
# For Team Project and Professionalism
## KV6002
""",
"deviceList":"""
shows the database stored devices, can be filtered by types, ids, and labelFilters

params in use:

- deviceTypes:list[str]|None=Query(default=None)
- deciveIds:list[str]|None=Query(default=None)
- labelFilters:list[str]|None=Query(default=None)
""",
"device":"""
Returns the database stored device specified in the url
""",
"project":"""
Returns the only project that will return data from other endpoints
""",
"projectList":"""
Returns fake projects hard coded into the API.
Projects aren't being used in this prototype and their existence is purely to match the Disruptive Systems API.
Shouldn't need dynamic for this prototype
""",
"eventHistory":"""
Retrieve a full list of all events for a device

params in use:
- project:str
- device:str
- eventTypes:Union[list[str],None]=Query(default=None)
- startTime:str=None
- endTime:str=None
""",
"emulate":"""
Runs the event emulaltion script to create a full set of events for each device in the database

Doesn't currently create events for cloud connector devices ("ccon")
""",
"esp32":"""
Returns all esp32 devices, functionally the same as requesting the devices endpoint with labelFilters parameter set to group=esp32, i.e:

`/projects/{project}/devices/{device}?labelFilters=group=esp32`
""",
"getAlerts":"""
## >CUSTOM< --needs auth

returns a list of alerts that have been set up
""",
"createAlerts":"""
## >CUSTOM< --needs auth

allows alerts to be created
""",
"updateAlerts":"""
## >CUSTOM< --needs auth

allows the updating of alerts
""",
"removeAlerts":"""
## >CUSTOM< --needs auth

allows the removal of alerts
""",
"createDevices":"""
## >CUSTOM< --needs auth

allows the creation of devices
""",
"updateDevices":"""
## >CUSTOM< --needs auth

allows the update of devices
""",
"removeDevices":"""
## >CUSTOM< --needs auth

allows the removal of devices
"""
}
tags_metadata = [
    {
        "name": "proto",
        "description": "Endpoints that exist only to serve the purpose of developing this prototype"
    },
    {
        "name": "Devices & Labels",
        "description": "DS endpoints about devices and labels."
    },
    {
        "name": "Event History",
        "description": "DS endpoit about event history"
    },
    {
        "name": "Organizations & Projects",
        "description": "DS endpoints about organizations and projects."
    },
    {
        "name": "Custom",
        "description": "Endpoints that aren't from the DS API"
    }
]