class dataFormatter:

    def project(this,
                name:str,displayName:str,sensorCount:int,cloudConnectorCount:int,
                organisation:str="b8ntihoaplm0028st07g",orgDisplayName:str="IoT Monitoring Inc."):
        """
        A JSON formatter for projects
        """
        return{
            "name":"projects/"+name,
            "displayName":displayName,
            "inventory":False,
            "organisation":"organizations/"+organisation,
            "organizationDisplayName": orgDisplayName,
            "sensorCount":sensorCount,
            "cloudConnectorCount":cloudConnectorCount
        }

    def cloudConnector(this,
            project_id:str,device_id:str,productNumber:str,labels:list[dict],
            connStatus_available:list[str]=["ETHERNET","CELLULAR"],connStatus_updateTime="time",
            ethernetStatus_macAddress:str="mac",ethernetStatus_ipAddress:str="ip",ethernetStatus_updateTime:str="time",
            cellularStatus_signalStrength:int=0,cellularStatus_updateTime:str="time",
            touch_updateTime:str="time"
            ):
        """
        A JSON formatter for cloud connector devices  
        """
        if "ETHERNET" in connStatus_available:
            connStatus_conn="ETHERNET"
        elif "CELLULAR" in connStatus_available:
            connStatus_conn="CELLULAR"
        else:
            connStatus_conn="OFFLINE"
        return {
            "name": "/projects/"+project_id+"/devices/"+device_id,
            "type": "ccon",
            "labels": labels,
            "reported": {
                "connectionStatus": {
                    "connection": connStatus_conn, #Either ETHERNET or CELLULAR - ETHERNET if available(see below) or OFFLINE if neither
                    "available": connStatus_available, #["ETHERNET"], ["CELLULAR"], ["ETHERNET","CELLULAR"] or []
                    "updateTime": connStatus_updateTime
                },
                "ethernetStatus": {
                    "macAddress": ethernetStatus_macAddress,
                    "ipAddress": ethernetStatus_ipAddress,
                    "errors": [
                        {"code": 404, "message": "Not found"},
                    ],
                    "updateTime": ethernetStatus_updateTime
                },
                "cellularStatus": {
                    "signalStrength": cellularStatus_signalStrength,
                    "errors": [
                        {"code": 404, "message": "Not found"},
                    ],
                    "updateTime": cellularStatus_updateTime
                },
                "touch": {
                    "updateTime": touch_updateTime
                }                
            },
            "productNumber": productNumber
        }
    

    def sensor(this,
            project_id:str,device_id:str,sensorType:str,productNumber:int,
            network_signalStrength:int=0,network_rssi:int=0,network_updateTime:str="time",
            network_ccon_id:int=0,network_ccon_signalStrength:int=0,network_ccon_rssi:int=0,
            battery_percentage:int=0,battery_updateTime:str="time",
            temp_temperature:float=0,temp_updateTime:str="time",
            humidity_temperature:float=0,humidity_relative:float=0,humidity_updateTime:str="time",
            co2_ppm:int=0,co2_updateTime:str="time"):
        """
        A JSON formatter for all sensor types
        """
        match sensorType:
            case "temperature":
                event=this.temperatureEvent(temperature=temp_temperature,updateTime=temp_updateTime)
            case "humidity":
                event=this.humidityEvent(temperature=humidity_temperature,humidity=humidity_relative,updateTime=humidity_updateTime)
            case "co2":
                event=this.co2Event(ppm=co2_ppm,updateTime=co2_updateTime)
            case _:
                return {"error":"invalid sensor type: "+sensorType}
        return {
                "name": "/projects/"+project_id+"/devices/"+device_id,
                "type": sensorType,
                "labels": {},
                "reported": {
                    "networkStatus": {
                        "signalStrength": network_signalStrength,
                        "rssi": network_rssi,
                        "updateTime": network_updateTime,
                        "cloudConnectors": [
                            {
                            "id": network_ccon_id,
                            "signalStrength": network_ccon_signalStrength,
                            "rssi": network_ccon_rssi
                            }
                        ],
                        "transmissionMode": "LOW_POWER_STANDARD_MODE"
                    },
                    "batteryStatus": {
                        "percentage": battery_percentage,
                        "updateTime": battery_updateTime
                    },
                    sensorType:event[sensorType]
                },
                "productNumber": productNumber
            }

        
    

    def temperatureEvent(this,temperature:float,updateTime:int):
        """"
        A JSON formatter for temperature events
        """
        return {
            "temperature": {
                "value": temperature,
                "updateTime": updateTime
            }
        }

    

    def humidityEvent(this,temperature:float=0,humidity:float=0,updateTime:str="time"):
        """
        A JSON formatter for humidity events
        """
        return {
            "humidity": {
                "temperature": temperature,
                "relativeHumidity": humidity,
                "updateTime": updateTime
            }
        }

    

    def co2Event(this,ppm:int=0,updateTime:str="time"):
        """
        A JSON formatter for co2 events
        """
        return {
            "co2": {
                "ppm": ppm,
                "updateTime": updateTime
            }
        }


# The following methods have been superseeded by the function sensor()
# However these have not been deleted until further testing

    # def temperatureSensor(this,
    #                       project_id:str,device_id:str,productNumber:int,
    #                       network_signalStrength:int=0,network_rssi:int=0,network_updateTime:str="time",
    #                       network_ccon_id:int=0,network_ccon_signalStrength:int=0,network_ccon_rssi:int=0,
    #                       battery_percentage:int=0,battery_updateTime:str="time",
    #                       temp_temperature:float=0,temp_updateTime:str="time"):
    #     """
    #     A JSON formatter for temperature sensors
    #     """
    #     return {
    #                 "name": "/projects/"+project_id+"/devices/"+device_id,
    #                 "type": "temperature",
    #                 "labels": {},
    #                 "reported": {
    #                     "networkStatus": {
    #                         "signalStrength": network_signalStrength,
    #                         "rssi": network_rssi,
    #                         "updateTime": network_updateTime,
    #                         "cloudConnectors": [
    #                             {
    #                             "id": network_ccon_id,
    #                             "signalStrength": network_ccon_signalStrength,
    #                             "rssi": network_ccon_rssi
    #                             }
    #                         ],
    #                         "transmissionMode": "LOW_POWER_STANDARD_MODE"
    #                     },
    #                     "batteryStatus": {
    #                         "percentage": battery_percentage,
    #                         "updateTime": battery_updateTime
    #                     },
    #                     "temperature": {
    #                     "value": temp_temperature,
    #                     "updateTime": temp_updateTime
    #                     }
    #                 },
    #                 "productNumber": productNumber
    #             }

    # def humiditySensor(this,
    #                       project_id:str,device_id:str,productNumber:int,
    #                       network_signalStrength:int=0,network_rssi:int=0,network_updateTime:str="time",
    #                       network_ccon_id:int=0,network_ccon_signalStrength:int=0,network_ccon_rssi:int=0,
    #                       battery_percentage:int=0,battery_updateTime:str="time",
    #                       humidity_temperature:float=0,humidity_relative:float=0,humidity_updateTime:str="time"):
    #     """
    #     A JSON formatter for humidity sensors
    #     """
    #     return {
    #                 "name": "/projects/"+project_id+"/devices/"+device_id,
    #                 "type": "temperature",
    #                 "labels": {},
    #                 "reported": {
    #                     "networkStatus": {
    #                         "signalStrength": network_signalStrength,
    #                         "rssi": network_rssi,
    #                         "updateTime": network_updateTime,
    #                         "cloudConnectors": [
    #                             {
    #                             "id": network_ccon_id,
    #                             "signalStrength": network_ccon_signalStrength,
    #                             "rssi": network_ccon_rssi
    #                             }
    #                         ],
    #                         "transmissionMode": "LOW_POWER_STANDARD_MODE"
    #                     },
    #                     "batteryStatus": {
    #                         "percentage": battery_percentage,
    #                         "updateTime": battery_updateTime
    #                     },
    #                     "humidity": {
    #                         "temperature": humidity_temperature,
    #                         "relativeHumidity": humidity_relative,
    #                         "updateTime": humidity_updateTime
    #                     }
    #                 },
    #                 "productNumber": productNumber
    #             }
    
    # def co2Sensor(this,
    #                 project_id:str,device_id:str,productNumber:int,
    #                 network_signalStrength:int=0,network_rssi:int=0,network_updateTime:str="time",
    #                 network_ccon_id:int=0,network_ccon_signalStrength:int=0,network_ccon_rssi:int=0,
    #                 battery_percentage:int=0,battery_updateTime:str="time",
    #                 co2_ppm:int=0,co2_updateTime:str="time"):
    #     """
    #     A JSON formatter for co2 sensors
    #     """
    #     return {
    #                 "name": "/projects/"+project_id+"/devices/"+device_id,
    #                 "type": "temperature",
    #                 "labels": {},
    #                 "reported": {
    #                     "networkStatus": {
    #                         "signalStrength": network_signalStrength,
    #                         "rssi": network_rssi,
    #                         "updateTime": network_updateTime,
    #                         "cloudConnectors": [
    #                             {
    #                             "id": network_ccon_id,
    #                             "signalStrength": network_ccon_signalStrength,
    #                             "rssi": network_ccon_rssi
    #                             }
    #                         ],
    #                         "transmissionMode": "LOW_POWER_STANDARD_MODE"
    #                     },
    #                     "batteryStatus": {
    #                         "percentage": battery_percentage,
    #                         "updateTime": battery_updateTime
    #                     },
    #                     "co2": {
    #                         "ppm": co2_ppm,
    #                         "updateTime": co2_updateTime
    #                     }
    #                 },
    #                 "productNumber": productNumber
    #             }
    
