from api.dbConnect import *

class deviceManager:
    def __init__(this):
        this.db=dbConnect()

    def getDeviceIDFromName(this,device_name:str,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        sqlGetId="SELECT device_id FROM devices WHERE device_name = '{}'".format(device_name)
        rows=this.db.run_query(sqlGetId)
        if len(rows)==0:
            return {"error":"device_name {} not found".format(device_name)}
        device_id=rows[0][0]
        return {"device_id":device_id}

    def getDeviceFormatted(this,device_id:int=None,device_name:str=None):
        query="""
        SELECT device_name, type, group_name, show, product_number
        FROM devices
        LEFT JOIN groups 
        ON devices.group_id=groups.group_id
        """
        if device_id is not None:
            sqlWhere = "WHERE device_id = '{}'".format(device_id)
        else:
            sqlWhere = "WHERE device_name = '{}'".format(device_name)
        query+=sqlWhere
        rows=this.db.run_query(query)
        output=[]
        
        output.append({
            "name":"projects/i7prjqnb2c4b6rob9xc2/devices/"+rows[0][0],
            "type":rows[0][1],
            "labels":{
                "group":rows[0][2],
                "show":rows[0][3]  
            },
            "productNumber":rows[0][4]
        })
        return output

    def createDevice(this,device_type:str,device_name:str,product_number:int,show:int=1,group_name:str=None,group_id=None,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        

        if device_type not in ["temperature", "humidity", "co2", "ccon"]:
            return {"error": "device_type {} not recognised".format(device_type)}
        if show not in [0,1]:
            return {"error": "show value {} not recognised, must be 0 or 1".format(show)}


        sqlCheckExisting="SELECT device_id, group_id, type, show, device_name, product_number FROM devices WHERE device_name='{}'".format(device_name)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)>0:
            return {"error":"device_name {} already in database".format(device_name)}
        
        if group_name is not None:
            sqlGetGroupId="SELECT group_id FROM groups WHERE group_name='{}'".format(group_name)
            rows=this.db.run_query(sqlGetGroupId)
            if len(rows)==0:
                return {"error":"group_name {} not recognised".format(group_name)}
            group_id=rows[0][0]
        sqlCreateDevice="INSERT INTO devices (group_id, type, show, device_name, product_number) VALUES ('{}','{}','{}','{}','{}')".format(group_id,device_type,show,device_name,product_number)
        this.db.run_insert(sqlCreateDevice)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"Device Not found in database after insert"}
        output=this.getDeviceFormatted(device_name=device_name)
        return {"message":"success","new device":output}

    def updateDevice(this,device_id:int,device_type:str=None,device_name:str=None,product_number:int=None,show:int=None,group_name:str=None,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        if device_id is None and device_type is None and device_name is None and product_number is None and show is None and group_name is None:
            return {"error":"no new values given"}
        
        if (device_type not in ["temperature", "humidity", "co2", "ccon"]) and device_type is not None:
            return {"error": "device_type {} not recognised".format(device_type)}
        if (show not in [0,1]) and show is not None:
            return {"error": "show value {} not recognised, must be 0 or 1".format(show)}

        #make sure that the device_name doesn't already exist in the database
        sqlCheckExistingName="SELECT device_id FROM devices WHERE device_name='{}'".format(device_name)
        rows=this.db.run_query(sqlCheckExistingName)
        if len(rows)>0:
            return {"error":"the device_name {} already exists, device_names must be unique".format(device_name)}

        sqlCheckExistingID="SELECT device_id, group_id, type, show, device_name, product_number FROM devices WHERE device_id='{}'".format(device_id)
        rows=this.db.run_query(sqlCheckExistingID)
        if len(rows)==0:
            return {"error":"unrecognised device_id"}

        sqlSetList=[]
        if device_type is not None:
            sqlSetList.append("type = '{}'".format(device_type))
        if device_name is not None:
            sqlSetList.append("device_name = '{}'".format(device_name))
        if product_number is not None:
            sqlSetList.append("product_number = '{}'".format(product_number))
        if show is not None:
            sqlSetList.append("show = '{}'".format(show))
        if group_name is not None:
            sqlGetGroupId="SELECT group_id FROM groups WHERE group_name='{}'".format(group_name)
            rows=this.db.run_query(sqlGetGroupId)
            if len(rows)==0:
                return {"error":"group_name {} not recognised".format(group_name)}
            group_id=rows[0][0]
            sqlSetList.append("group_id = '{}'".format(group_id))
        sqlSet=sqlSetList[0]
        if len(sqlSetList)>1:
            for i in range(1,len(sqlSetList)):
                sqlSet+=", "+sqlSetList[i]
        sqlUpdate="UPDATE devices SET {} WHERE device_id = '{}'".format(sqlSet,device_id)
        this.db.run_insert(sqlUpdate)
        

        rows=this.db.run_query(sqlCheckExistingID)
        if len(rows)==0:
            return {"error":"Device not found in database after update"}
        output=this.getDeviceFormatted(device_id=device_id)
        return {"message":"success","updated device":output}

    def removeDevice(this,device_id:int,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        sqlCheckExisting="SELECT * FROM devices WHERE device_id='{}'".format(device_id)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"unrecognised device_id"}
        

        sqlRemove="DELETE FROM devices WHERE device_id = '{}'".format(device_id)
        this.db.run_insert(sqlRemove)
        
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)!=0:
            return {"error":"device found in database after delete"}
        return {"message":"success"}
