# Team Project API

## API Information


**Deployed API**

The deployed version of the API is deployed on Microsoft Azure


**API Base URLs:**

The current active API can be found at the link here: [http://20.77.135.86](http://20.77.135.86/ "API version 4, uploaded 03/04/23")

A full list of active API versions can be found in the table below:


| URL | current? | active? | version | upload date |
| --- | --- | --- | --- | --- |
| `http://20.108.89.49` | old | active | version 2 | 23/03/2023 |
| `http://20.108.140.207/` | old | active | version 3 | 24/03/2023 |
| http://20.77.135.86 | current | active | version 4 | 03/04/2023 |

**How to run the API on a local machine**

To run the API on your computer, you need to download this repository and install:
- python 3.9 or above along with the libraries:
    - fastapi
    - sqlite3
    - httpx
    - datetime
    - random
    - typing
- uvicorn

Then navigate to the directory this readme file is located in and run the command:

`uvicorn main:app --reload`


# Disruptive Systems Endpoints

## DS Projects

**List Projects** - `/projects`
- List all the projects available to be used
- This endpoint exists in order to act more like the Disruptive Systems API, however it only returns a set hard-coded response as full functionality of multiple projects is not required for this prototype

---

**Single Project** - `/projects/{project}`
- List the details of a single project with the 'id' of {project}
- Functionality in order to act like the DS API, only returns a set response - doesn't retrieve data from the database
- Only project id that retrieves a response is `i7prjqnb2c4b6rob9xc2` - all following DS style endpoints will require this id in the URL in the place of {project}

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `project` | _str_ | _required_ | Id of the project that is being retrieved |

---

## DS Devices

**List Devices** - `/projects/{project}/devices`
- Show a list of all devices in the project. The parameters `deviceIds`, `deviceTypes`, and `labelFilters` can be used to filter the list, these all can be combined to achieve further filtering.

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `project` | _str_ | _required_| The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API |
| `deviceIds` | _list[str]_ | _default:None_  | A list of device ids to filter the devices with |
| `deviceTypes` | _list[str]_ | _default:None_  | A list of device types to filter the devices with, each type can be one of the following: "temperature", "humidity", "co2", or "ccon"; with ccon standing for 'cloud connector' - the device used to connect the sensors to the internet |
| `labelFilters` | _list[str]_ | _default:None_  | A list of labelFilters to filter the devices with, labels exist as key value pairs, with 2 implemented in this prototype: "group", and "show". An example of the parameter value could be `group=East Wing` or `show=1` so at the end of the devices endpoint the paramater may look like `?labelFilters=group=East Wing` or `?labelFilters=show=1`  |

---

**Single Device** - `/projects/{project}/devices/{device}`
- Show the information of one device with the 'id' of {device}

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `project` | _str_ | _required_ | The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API |
| `device` | _str_ | _required_ | The id of a device that is to be retrieved |

---

## DS Events

**List Device Events** - `/projects/{project}/devices/{device}`
- List all events of one device with id of {device}. Uses of datetime in this endpoint are formatted into strings using the following format: "`yyyy`-`mm`-`dd`T`HH`:`MM`:`SS`Z"
  - `y` representing year digits
  - `m` representing month digits
  - `d` representing day digits
  - `H` representing hour digits
  - `M` representing minute digits
  - `S` representing second digits

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `project` | _str_ | _required_ | The id of the project that is being accessed, `i7prjqnb2c4b6rob9xc2` is the only project accessible in this API |
| `device` | _str_ | _required_ | The id of a device that is to be retrieved |
| `eventTypes` | _list[str]_ | _default:None_ | A list of eventTypes to filter the results by, usable eventTypes are:  "temperature", "humidity", "co2", "batteryStatus", "networkStatus", "touch", "connectionStatus", "ethernetStatus", "cellularStatus" |
| `startTime` | _str_ | _default:(now-24hours)_ | The start time of when to filter for events in datetime form, by default this is 24 hours before the current time |
| `endTime` | _str_ | _default:(now)_ | The end time of when to filter for events in datetime form, by default this is the current time |

---

# Custom Endpoints

## Prototype Endpoints

**Emulate** - `/emulate`
- Runs the script to create a full set of emulated values for all devices stored in the database.
- This does not take parameters.
- This endpoint is only used for the purposes of prototyping and will not feature in the final system
- Note: The datetimes generated by this endpoint do not account for daylights savings or any other localisation of time zones. However as this is just a prototype feature, and such localisation would usually be handled by the front end application, this is not an issue

---

**Esp32** - `/esp32`
- Returns data about all the esp32 based devices available. This funtions the same as using the endpoint `/projects/{project}/devices` with the parameter `labelFilers` set to `group=esp32`
- This does not take parameters.
- This endpoint is only used for the purposes of prototyping and will not feature in the final system

---

## Alert Management

**Get Alerts** - `/alerts`
- Retrieves alerts from database

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `employee_id` | _int_ | _default:None_  | ID of the employee that will recieve the email alert, used to filter results by. Must be an existing employee_id in database or the error `"employee_id {} not found"` will be returned |
| `type` | _str_ | _default:None_  | Type of device the alert is attatched, used to filter results by. Must be one of "temperature","humidity","co2","ccon" or the error `"unknown type {}"` will be returned |

---

**Create Alert** - `/alerts/create`
- Creates an alert in database. Must have at least one value be unique or the error `"exact alert found in database"` is returned

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `employee_id` | _int_ | _required_ | ID of the employee that will recieve the email alert |
| `device_name` | _str_ | _required_ | Name of device the alert is attatched to, must exist in database or the `"unrecognised device_name {}"` will be returned |
| `threshold` | _float_ | _required_ | The threshold at which the alert should trigger |
| `max` | _int_ | _required_ | Whether the alert should be triggered when the device's value rises to/above the threshold (`max` value of `1`), or falls to/below (`max` value of `0`). Must be either `1` or `0` otherwise the error `"max value {} not recognised, must be 0 or 1"` will be returned |

---

**Update Alert** - `/alerts/update/{alert_id}`
- Updates alert with an id of {alert_id} in database, any parameter that is not required will not update the database if not changed from default value. If none of the non-required parameters are set then the error `"no new values given"` will be returned

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `alert_id` | _int_ | _required_ | ID of the alert to be updated, must exist in the database or the error `"unrecognised alert_id {}"` will be returned|
| `employee_id` | _int_ | _default:None_  | ID of the employee that will recieve the email alert, must exist in the database or the error `"unrecognised employee_id {}"` will be returned |
| `device_name` | _str_ | _default:None_  | Name of the device attatched to the alert, must exist in the database or the error `"unrecognised device_id {}"` will be returned |
| `threshold` | _float_ | _default:None_  | The threshold at which the alert should trigger |
| `max` | _int_ | _default:None_  | Whether the alert should be triggered when the device's value rises to/above the threshold (`max` value of `1`), or falls to/below (`max` value of `0`). Must be either `1` or `0` otherwise the error `"max value {} not recognised, must be 0 or 1"` will be returned |

---

**Remove Alert** - `/alerts/remove/{alert_id}`
- Removes alert with an id of {alert_id}. If the alert_id is still found in the database after deletion, then the error `"alert with alert_id={} found in database after deletion"`

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `alert_id` | _int_ | _required_ | id of the alert to be deleted, must exist in the database or the error `"unrecognised alert_id {}"` will be returned |

---

## Device Management

**Create Device** - `/devices/create`
- Create new devices in the database

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `device_type` | _str_ | _required_ | Type of device, must be one of: "temperature", "humidity", "co2", or "ccon"  _(with "ccon" standing for "cloud connector");_ or the error `"device_type {} not recognised"` is returned |
| `device_name` | _str_ | _required_ | Id of the device, must be unique or the error `"device_name already in database"` will be returned |
| `product_number` | _int_ | _required_ | The product number assigned to the device |
| `show` | _int_ | _default:1_ | Whether the device should be shown in the public display, acts a boolean with `0` = `False` and `1` = `True`. Must be either `1` or `0` or the error `"show value {} not recognised, must be 0 or 1"` will be returned |
| `group_name` | _str_ | _default:None_ | Name of group the device should be in, must be a group that already exists in the database or the error `"group_name {} not recognised"` will be returned |

---

**Update Device** - `/devices/update/{device}`
- Updates a device in the database with the id {device}
- The current id of the device goes into the url path parameter {device} as shown above, if you wish to change the name, then use the parameter device_name as listed below
- If none of the non-required parameters are set then the error `"no new values given"` will be returned

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `device` | _int_ | _required_ | The id of the device to be updated, must be an existing device id or the error `"unrecognised device {}"` will be returned |
| `device_type` | _str_ | _default:None_ | Type of device, must be one of: "temperature", "humidity", "co2" or "ccon", else the error `"device_type {} not recognised"` will be returned |
| `device_name` | _str_ | _default:None_ | New id of the device, must be unique to the database or will return error `"device_name {} already in database"`|
| `product_number` | _int_ | _default:None_ | The product number assigned to the device |
| `show` | _int_ | _default:None_ | Whether the device should be shown in the public display, acts a boolean with `0` = `False` and `1` = `True`. Must be either `1` or `0` or the error `"show value {} not recognised, must be 0 or 1"` will be returned |
| `group_name` | _str_ | _default:None_ | Name of the group the device should be in, must be a group that already exists in the database or the error `"group_name {} not recognised"` will be returned |

---

**Remove Device** - `/devices/remove/{device}`
- Deletes a device in the database with the id of {device}
- Validates that the device exists before trying to delete and will return an error if it does not exist

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `device` | _int_ | _required_ | The id of the device to be deleted, must exist in the database or the error `"unrecognised device_id"` will be returned |

---

## Employee Management

**Get Employees** - `/employees`
- Returns information about the employees
- Note: the current prototype stores the employees passwords as plain text, this will be encrypted in the final version, however as these are only being used for testing this has not been implemented yet

| Paramater Name | Datatype | Required / Default | Description |
|---|---|---|---|
| `employee_ids` | _list[int]_ | _default:None_ | A list of employee ids used in the database, this can be used for filtering with as many employee ids as needed|

---
