class device:

    _data:dict

    def __init__(this,project_id:str,device_id:str,sensorType:str,productNumber:int,
            network_signalStrength:int=0,network_rssi:int=0,network_updateTime:str="time",
            network_ccon_id:int=0,network_ccon_signalStrength:int=0,network_ccon_rssi:int=0,
            battery_percentage:int=0,battery_updateTime:str="time"):
        this._data={
            "project_id":project_id,
            "device_id":device_id,
            "sensorType":sensorType,
            "productNumber":productNumber,
            "network_signalStrength":network_signalStrength,
            "network_rssi":network_rssi,
            "network_updateTime":network_updateTime,
            "network_ccon_id":network_ccon_id,
            "network_ccon_signalStrength":network_ccon_signalStrength,
            "network_ccon_rssi":network_ccon_rssi,
            "battery_percentage":battery_percentage,
            "battery_updateTime":battery_updateTime
        }

    def getData(this):
        return this._data


class dataRead:
    _deviceList:list[device]
    def __init__(this):
        this._deviceList.append(device())