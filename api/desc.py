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

- deviceTypes:list[str]|None=Query(default=None)
- deciveIds:list[str]|None=Query(default=None)


unused params:

- labelFilters:list[str]|None=Query(default=None)
- orderBy:str=None
- query:str=None
- productNumbers:list[str]|None=Query(default=None)
- pageSize:int=None
- pageToken:str=None
""",
"device":"""
Returns the given projects and device number in an otherwise empty temp sensor JSON object

params in use:

unused params:
- project:str
- device:str
- sensorType:str
""",
"project":"NOT CURRENTLY IN USE---PAGE UNDER CONSTRUCTION",
"projectList":"""
Shows list of projects

params in use:

unused params:
- query:str=""
- pageSize:int=10
- pageToken:int=0
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
        "name": "Organizations & Projects",
        "description": "DS endpoints about organizations and projects."
    },
    {
        "name": "Not Implemented",
        "description": "These endpoints have not been implemented yet."
    }
]