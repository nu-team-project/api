from api.dbConnect import *

class alertManager:
    def __init__(this):
        this.db=dbConnect()

    def getAlerts(this,auth:bool=True,employee_id:int=None,type:str=None,event_id:int=None):
        if not auth:
            return {"error":"authorisation failed"}
        where:str=None
        query="SELECT alert_id, employee_id, device_name, type, threshold, max FROM alerts INNER JOIN devices ON alerts.device_id = devices.device_id"
        if employee_id is not None:
            where=(" WHERE" if where is None else where+" AND")+(" employee_id="+str(employee_id))
        if type is not None:
            where=(" WHERE" if where is None else where+" AND")+(" type="+type)
        if event_id is not None:
            where=(" WHERE" if where is None else where+" AND")+(" event_id="+str(event_id))
        if where is not None:
            query+=where
        rows=this.db.run_query(query)
        output=[]
        columns=["alert_id", "employee_id", "device_name", "type", "threshold", "max"]
        for each in rows:
            alert={}
            for i in range(len(columns)):
                alert[columns[i]]=each[i]
            output.append(alert)
        return {"auth":"success","length":len(rows),"message":output}

        
    def __checkVariableTypes(this,variablesAndTypeList:list[dict]):
        output=[]
        for each in variablesAndTypeList:
            error=False
            if each["type"]==str and type(each["value"])!=str:
                error=True
            elif each["type"]==int:
                try:
                    int(each["value"])
                except:
                    error=True
            elif each["type"]==float:
                try:
                    float(each["value"])
                except:
                    error=True
            elif each["type"]==bool and each["value"] not in [0,1]:
                error=True
            elif each["type"]=="device_type" and each["value"] not in ["ccon","temperature","humidity","co2"]:
                error=True
            if error:
                output.append("Incorrect parameter type for "+each["variableName"]+". Should be "+str(each["type"])+" but equals: "+str(each["value"]))
        return output

    def createAlerts(this,employee_id:int,device_name:str,threshold:float,max:int,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        typeErrors=this.__checkVariableTypes([
            {"variableName":"employee_id","type":int,"value":employee_id},
            {"variableName":"device_name","type":str,"value":device_name},
            {"variableName":"threshold","type":float,"value":threshold},
            {"variableName":"max","type":bool,"value":max}])
        if len(typeErrors)>0:
            return{"errors":typeErrors}
        
        sqlCheckExisting="""
        SELECT alert_id, employee_id, device_name, type, threshold, max
        FROM alerts 
        INNER JOIN devices 
        ON alerts.device_id=devices.device_id 
        WHERE employee_id="{}" 
        AND device_name="{}"
        AND threshold="{}"
        AND max="{}"
        """.format(employee_id,device_name,threshold,max)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)>0:
            return {"error":"This exact alert already exists"}
        
        sqlGetDeviceId="SELECT device_id FROM devices WHERE device_name='{}'".format(device_name)
        rows=this.db.run_query(sqlGetDeviceId)
        print(rows)
        device_id=rows[0][0]
        sqlCreateAlert="INSERT INTO alerts (employee_id, device_id, threshold, max) VALUES ('{}','{}','{}','{}')".format(employee_id,device_id,threshold,max)
        this.db.run_insert(sqlCreateAlert)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"Alert Not found in database after insert"}
        
        output=[]
        columns=["alert_id", "employee_id", "device_name", "type", "threshold", "max"]
        for each in rows:
            alert={}
            for i in range(len(columns)):
                alert[columns[i]]=each[i]
            output.append(alert)
        return {"message":"success","newAlert":output}
    
    def updateAlerts(this,alert_id:int,employee_id:int=None,device_id:int=None,threshold:float=None,max:int=None,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        if employee_id is None and device_id is None  is None and threshold is None and max is None:
            return {"error":"no new values given"}
        
        #validate data
        #-check values are correct type
        typeErrors=this.__checkVariableTypes([{"variableName":"alert_id","type":int,"value":alert_id}])
        if employee_id is not None:
            typeErrors+=this.__checkVariableTypes([{"variableName":"employee_id","type":int,"value":employee_id}])
        if device_id is not None:
            typeErrors+=this.__checkVariableTypes([{"variableName":"device_name","type":str,"value":device_id}])
        if threshold is not None:
            typeErrors+=this.__checkVariableTypes([{"variableName":"threshold","type":float,"value":threshold}])
        if max is not None:
            typeErrors+=this.__checkVariableTypes([{"variableName":"max","type":bool,"value":max}])
        if len(typeErrors)>0:
            return{"errors":typeErrors}
        
        #-check if alert exists
        sqlCheckExisting="SELECT * FROM alerts WHERE alert_id='{}'".format(alert_id)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"unrecognised alert_id"}

        #execute query
        sqlSetList=[]
        if employee_id is not None:
            sqlSetList.append("employee_id = '{}'".format(employee_id))
        if device_id is not None:
            sqlSetList.append("device_id = '{}'".format(device_id))
        if threshold is not None:
            sqlSetList.append("threshold = '{}'".format(threshold))
        if max is not None:
            sqlSetList.append("max = '{}'".format(max))
        sqlSet=sqlSetList[0]
        if len(sqlSetList)>1:
            for i in range(1,len(sqlSetList)):
                sqlSet+=", "+sqlSetList[i]
        sqlUpdate="UPDATE alerts SET {} WHERE alert_id = '{}'".format(sqlSet,alert_id)
        print("debug>>sqlUpdate = {}".format(sqlUpdate))
        this.db.run_insert(sqlUpdate)
        

        #return errors
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"Alert not found in database after update"}
        
        #return success message
        #-success message can include alert newly retrieved
        output=[]
        columns=["alert_id", "employee_id", "device_id", "threshold", "max"]
        for each in rows:
            alert={}
            for i in range(len(columns)):
                alert[columns[i]]=each[i]
            output.append(alert)
            return {"message":"success", "updated alert": output}
        
    def removeAlerts(this,alert_id:int,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        #validate data
        #-check if alert exists
        sqlCheckExisting="SELECT * FROM alerts WHERE alert_id='{}'".format(alert_id)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"unrecognised alert_id"}
        
        #execute query
        sqlRemove="DELETE FROM alerts WHERE alert_id = '{}'".format(alert_id)
        this.db.run_insert(sqlRemove)
        

        #return errors/success message
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)!=0:
            return {"error":"alert found in database after delete"}
        return {"message":"alert removed"}