# Team Project API

## [Link To Website Repository](https://github.com/nu-team-project/website)

---



# Deployed API

The deployed version of the API is deployed on Microsoft Azure

---

## API Base:

A list of all active api bases are listed here, all links in the rest of this document will use the api base marked 'current'

[`https://20.108.140.207/`](https://20.108.140.207/ "v2 uploaded _24/03/2023_")  - current

[`http://20.108.89.49/`](http://20.108.89.49/ "v1 uploaded _23/03/2023_") - old


---

**New to this api version** - Access to the esp32 based sensors

The esp32 based sensors can be reached using the labelFilter `group=esp32` on the  [`devices`](https://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices) endpoint, or by using the endpoint [`/esp32`](https://20.108.140.207/esp32), this extra endpoint is not the proper way to access the data but could be useful while protoyping

---

## How to get data from the API:

Devices are found on the endpoint [`http://20.108.89.49/projects/i7prjqnb2c4b6rob9xc2/devices`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices)

These devices can be filtered by group using the path parameter `labelFilters` and setting that equal to `group=` and then the group name

There is a group of sensors called `Model` so this can be requested at [`http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model)

There are currently 5 such groups available in the database:
- `Model`
- `esp32`
- `East Wing`
- `West Wing`
- `South Wing`

Multiple groups can be requested simply by adding that to the path e.g. [`http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model&labelFilters=group=East%20Wing`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model&labelFilters=group=East%20Wing)
_(`%20` used as a space in the url here)_

If you want to filter by device type then use the path parameter `deviceTypes` and set it equal to one of the 4 available device types:
- `temperature`
- `humidity`
- `co2`
- `ccon`

_(`ccon` is the name used for cloud connectors, the box that connects sensors to the cloud)_

An example endpoint for all `temperature` devices is: [`http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature)

This can be combined for multiple device types the same way that the group path parameter can [`http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature&deviceTypes=co2`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?deviceTypes=temperature&deviceTypes=co2)

This can also be combined with the group parameter to, for example, get the `temperature` sensor from the group `Model`: [`http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model&deviceTypes=temperature`](http://20.108.140.207/projects/i7prjqnb2c4b6rob9xc2/devices?labelFilters=group=Model&deviceTypes=temperature)

---



## How to update the emulated API data:

This will be automated soon and run every 15 minutes when it is, but until then the emulation script can be run by sending a get reqeust to the endpoint `/emulate`:

[`http://20.108.140.207/emulate`](http://20.108.140.207/emulate)


---

## How to run the API on a local machine

To run the API on your computer, you need python, FastAPI, and uvicorn installed, then run the command:

`uvicorn main:app --reload`

assuming the file with the API code is called `main` and the FastAPI python object is called `app`

---

## Useful Links

- [Disruptive Technologies API Reference](https://developer.disruptive-technologies.com/api )
- Python Libraries:
    - [FastAPI](fastapi.tiangolo.com)
    - [Uvicorn](www.uvicorn.org)
- [Markdown Syntax Reference](https://www.markdownguide.org/basic-syntax/)