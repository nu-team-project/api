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

unused params:

- orderBy:str=None
- query:str=None
- productNumbers:list[str]|None=Query(default=None)
- pageSize:int=None
- pageToken:str=None
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

params in use:

unused params:
- query:str=""
- pageSize:int=10
- pageToken:int=0
""",
"eventHistory":"""
Soon to be implemented

params in use:

unused params:
"""
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
        "name": "Event History",
        "description": "DS endpoit about event history"
    },
    {
        "name": "Organizations & Projects",
        "description": "DS endpoints about organizations and projects."
    }
]