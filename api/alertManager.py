from api.dbConnect import *

class alertManager:
    def __init__(this):
        this.db=dbConnect()

    def getAlerts(this,auth:bool=True,employee_id:int=None,type:str=None):
        if not auth:
            return {"error":"authorisation failed"}
        where:str=None
        query="SELECT alert_id, employee_id, device_name, type, threshold, max FROM alerts INNER JOIN devices ON alerts.device_id = devices.device_id"
        if employee_id is not None:
            sql_checkEmployeeId="Select * from employees where employee_id = {}".format(employee_id)
            rows=this.db.run_query(sql_checkEmployeeId)
            if len(rows)==0:
                return {"error":"employee_id {} not found".format(employee_id)}
            where=(" WHERE" if where is None else where+" AND")+(" employee_id="+str(employee_id))
        if type is not None:
            if type not in ["temperature","humidity","co2","ccon"]:
                return {"error","unknown type {}".format(type)}
            where=(" WHERE" if where is None else where+" AND")+(" type="+type)
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
        return {"message":"success","alerts":output}
        
       
    def createAlerts(this,employee_id:int,device_name:str,threshold:float,max:int,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        if max not in [0,1]:
            return {"error": "max value {} not recognised, must be 0 or 1".format(max)}
        
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
            return {"error":"exact alert found in database"}
        
        sqlGetDeviceId="SELECT device_id FROM devices WHERE device_name='{}'".format(device_name)
        rows=this.db.run_query(sqlGetDeviceId)
        if len(rows)==0:
            return {"error":"unrecognised device_name {}".format(device_name)}
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
    
    def updateAlerts(this,alert_id:int,employee_id:int=None,device_name:int=None,threshold:float=None,max:int=None,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        #check max is treated as a boolean if set
        if (max not in [0,1]) and max is not None:
            return {"error": "max value {} not recognised, must be 0 or 1".format(max)}

        #if set, check that the employee_id exists in the database
        if employee_id is not None:
            sqlCheckEmployee="SELECT * FROM employees WHERE employee_id='{}'".format(employee_id)
            rows=this.db.run_query(sqlCheckEmployee)
            if len(rows)==0:
                return {"error":"unrecognised employee_id {}".format(employee_id)}
            
        #if set, check that the device_name exists in the database and get the database id for it
        if device_name is not None:
            sqlCheckDeviceName="SELECT device_id FROM devices WHERE device_name='{}'".format(device_name)
            rows=this.db.run_query(sqlCheckDeviceName)
            if len(rows)==0:
                return {"error":"unrecognised device_id {}".format(device_name)}
            device_id=rows[0][0]
        else:
            device_id=None

        #check if any optional parameters have actually been set, and return an error if not
        if employee_id is None and device_name is None  is None and threshold is None and max is None:
            return {"error":"no new values given"}
   
        #check that there is an alert with that alert_id in the database
        sqlCheckAlertId="SELECT alert_id, employee_id, device_id, threshold, max FROM alerts WHERE alert_id='{}'".format(alert_id)
        rows=this.db.run_query(sqlCheckAlertId)
        if len(rows)==0:
            return {"error":"unrecognised alert_id {}".format(alert_id)}
        
        #build the query regardless of how many of the paramaters are set or not, then run the update query
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
        this.db.run_insert(sqlUpdate)
        
        #check that the device_id still exists in the database and hasn't been corrupted/lost
        rows=this.db.run_query(sqlCheckAlertId)
        if len(rows)==0:
            return {"error":"Alert not found in database after update"}
        
        #format the updated data to be output as easier to read json and return it
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
            return {"error":"unrecognised alert_id {}".format(alert_id)}
        
        #execute query
        sqlRemove="DELETE FROM alerts WHERE alert_id = '{}'".format(alert_id)
        this.db.run_insert(sqlRemove)
        

        #return errors/success message
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)!=0:
            return {"error":"alert with alert_id={} found in database after deletion".format(alert_id)}
        return {"message":"success"}