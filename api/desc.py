AppData={
    "title":"Prototype Environment Sensor API",
    "desc":"""
# For Team Project and Professionalism
## KV6002 - Team 9
""",
    "version":"4"
}
Desc={}
Desc["projectList"]="""
List all the projects available to be used.

This endpoint exists in order to act more like the Disruptive Systems API, however it only returns a set hard-coded response as full functionality of multiple projects is not required for this prototype
"""
Desc["project"]="""
List the details of a single project with the 'id' of {project}

Functionality in order to act like the Disruptive Systems API, only returns a set response - doesn't retrieve data from the database

Only project id that retrieves a response is `i7prjqnb2c4b6rob9xc2` - all following DS style endpoints will require this id in the URL in the place of {project}
"""
Desc["deviceList"]="""Show a list of all devices in the project.

The parameters `deviceIds`, `deviceTypes`, and `labelFilters` can be used to filter the list, these all can be combined to achieve further filtering."""
Desc["device"]="""Show the information of one device with the 'id' of {device}"""
Desc["eventHistory"]="""
List all events of one device with id of {device}. Uses of datetime in this endpoint are formatted into strings using the following format:

`yyyy`-`mm`-`dd`T`HH`:`MM`:`SS`Z
  - `y` representing year digits
  - `m` representing month digits
  - `d` representing day digits
  - `H` representing hour digits
  - `M` representing minute digits
  - `S` representing second digits
"""
Desc["emulate"]="""
Runs the event emulation script to create a full set of events for each device in the database

Doesn't currently create events for cloud connector devices ("ccon")
"""
Desc["esp32"]="""
Returns all esp32 devices, functionally the same as requesting the devices endpoint with labelFilters parameter set to group=esp32, i.e:

`/projects/{project}/devices/{device}?labelFilters=group=esp32`
"""
Desc["getAlerts"]="""Retrieves alerts from database"""
Desc["createAlerts"]="""Creates an alert in database. Must have at least one value be unique or the error `"exact alert found in database"` is returned"""
Desc["updateAlerts"]="""Updates alert with an id of {alert_id} in database, any parameter that is not required will not update the database if not changed from default value. If none of the non-required parameters are set then the error `"no new values given"` will be returned"""
Desc["removeAlerts"]="""Removes alert with an id of {alert_id}. If the alert_id is still found in the database after deletion, then the error `"alert with alert_id={} found in database after deletion"`"""
Desc["createDevices"]="""Create new devices in the database"""
Desc["updateDevices"]="""
Updates a device in the database with the id {device}

The current id of the device goes into the url path parameter {device} as shown above, if you wish to change the name, then use the parameter device_name as listed below

If none of the non-required parameters are set then the error `"no new values given"` will be returned
"""
Desc["removeDevices"]="""
Deletes a device in the database with the id of {device}

Validates that the device exists before trying to delete and will return an error if it does not exist
"""
Desc["getEmployees"]="""
Returns information about the employees

Note: the current prototype stores the employees passwords as plain text, this will be encrypted in the final version, however as these are only being used for testing this has not been implemented yet
"""

QueryDesc={}
QueryDesc["/projects/project"]={
    "project":"Id of the project that is being retrieved"
}
QueryDesc["/projects/project/devices"]={
    "project":"The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API",
    "deviceIds":"A list of device ids to filter the devices with",
    "deviceTypes":'A list of device types to filter the devices with, each type can be one of the following: "temperature", "humidity", "co2", or "ccon"; with ccon standing for "cloud connector" - the device used to connect the sensors to the internet',
    "labelFilters":"A list of labelFilters to filter the devices with, labels exist as key value pairs, with 2 implemented in this prototype: 'group', and 'show'. An example of the parameter value could be `group=East Wing` or `show=1` so at the end of the devices endpoint the paramater may look like `?labelFilters=group=East Wing` or `?labelFilters=show=1`"
}
QueryDesc["/projects/project/devices/device"]={
    "project":"The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API",
    "device":"The id of a device that is to be retrieved"
}
QueryDesc["/projects/project/devices/device/events"]={
    "project":"The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API",
    "device":"The id of a device that is to be retrieved",
    "eventTypes":'A list of eventTypes to filter the results by, usable eventTypes are:  "temperature", "humidity", "co2", "batteryStatus", "networkStatus", "touch", "connectionStatus", "ethernetStatus", "cellularStatus"',
    "startTime":"The start time of when to filter for events in datetime form, by default this is 24 hours before the current time",
    "endTime":"The end time of when to filter for events in datetime form, by default this is the current time"
}
QueryDesc["/alerts"]={
    "employee_id":'Id of the employee that will recieve the email alert, used to filter results by. Must be an existing employee_id in database or the error `"employee_id {} not found"` will be returned',
    "type":'Type of device the alert is attatched, used to filter results by. Must be one of "temperature","humidity","co2","ccon" or the error `"unknown type {}"` will be returned'
}
QueryDesc["/alerts/create"]={
    "employee_id":'ID of the employee that will recieve the email alert, must exist in the database or the error `"unkown employee_id {}"` will be returned',
    "device_name":'Name of device the alert is attatched to, must exist in database or the `"unrecognised device_name {}"` will be returned',
    "threshold":'The threshold at which the alert should trigger',
    "max":"Whether the alert should be triggered when the device's value rises to/above the threshold (`max` value of `1`), or falls to/below (`max` value of `0`). Must be either `1` or `0` otherwise the error"+'`"max value {} not recognised, must be 0 or 1"` will be returned'
}
QueryDesc["/alerts/update/alert_id"]={
    "alert_id":'ID of the alert to be updated, must exist in the database or the error `"unrecognised alert_id {}"` will be returned',
    "employee_id":'ID of the employee that will recieve the email alert, must exist in the database or the error `"unrecognised employee_id {}"` will be returned',
    "device_name":'Name of the device attatched to the alert, must exist in the database or the error `"unrecognised device_id {}"` will be returned',
    "threshold":'The threshold at which the alert should trigger',
    "max":"Whether the alert should be triggered when the device's value rises to/above the threshold (`max` value of `1`), or falls to/below (`max` value of `0`). Must be either `1` or `0` otherwise the error"+'`"max value {} not recognised, must be 0 or 1"` will be returned'
}
QueryDesc["/alerts/remove/alert_id"]={
    "alert_id":'id of the alert to be deleted, must exist in the database or the error `"unrecognised alert_id {}"` will be returned'
}
QueryDesc["/devices/create"]={
    "device_type":'Type of device, must be one of: "temperature", "humidity", "co2", or "ccon"  _(with "ccon" standing for "cloud connector");_ or the error `"device_type {} not recognised"` is returned',
    "device_name":'Id of the device, must be unique or the error `"device_name already in database"` will be returned',
    "product_number":'The product number assigned to the device',
    "show":'Whether the device should be shown in the public display, acts a boolean with `0` = `False` and `1` = `True`. Must be either `1` or `0` or the error `"show value {} not recognised, must be 0 or 1"` will be returned',
    "group_name":'Name of group the device should be in, must be a group that already exists in the database or the error `"group_name {} not recognised"` will be returned',
}
QueryDesc["/devices/update/device"]={
    "device":'The id of the device to be updated, must be an existing device id or the error `"unrecognised device {}"` will be returned',
    "device_type":'Type of device, must be one of: "temperature", "humidity", "co2" or "ccon", else the error `"device_type {} not recognised"` will be returned',
    "device_name":'New id of the device, must be unique to the database or will return error `"device_name {} already in database"`',
    "product_number":'The product number assigned to the device',
    "show":'Whether the device should be shown in the public display, acts a boolean with `0` = `False` and `1` = `True`. Must be either `1` or `0` or the error `"show value {} not recognised, must be 0 or 1"` will be returned',
    "group_name":'Name of the group the device should be in, must be a group that already exists in the database or the error `"group_name {} not recognised"` will be returned',
}
QueryDesc["/devices/remove/device"]={
    "device":'The id of the device to be deleted, must exist in the database or the error `"unrecognised device {}"` will be returned'
}
QueryDesc["/employees"]={
    "employee_ids":"A list of employee ids used in the database, this can be used for filtering with as many employee ids as needed"
}




tags_metadata = [
    {
        "name": "Projects",
        "description": "Disruptive Systems style endpoints about projects."
    },
    {
        "name": "Devices & Labels",
        "description": "Disruptive Systems style endpoints about devices and labels."
    },
    {
        "name": "Event History",
        "description": "Disruptive Systems style endpoit about event history"
    },
    {
        "name": "Prototype",
        "description": "Endpoints that exist only to serve the purpose of developing this prototype and will not feature in a full release"
    },
    {
        "name": "Alert Management",
        "description": "Endpoints that are used to retrieve, create, change, and delete alert data"
    },
    {
        "name": "Device Management",
        "description": "Endpoints that are used to create, change, and delete device data"
    },
    {
        "name": "Employee Management",
        "description": "Endpoints that are used to retrieve employee data"
    }
]