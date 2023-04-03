from api.dbConnect import *

class alertManager:
    def __init__(this):
        this.db=dbConnect()

    def getAlerts(this,auth:bool=True,employee_id:int=None,type:str=None):
        if not auth:
            return {"error":"authorisation failed"}
        
        where=""
        query="SELECT alert_id, employee_id, device_name, type, threshold, max FROM alerts INNER JOIN devices ON alerts.device_id = devices.device_id"
        
        #if an employee_id has been provided then check it exists, returning an error if not or adding it to the sql query if it does 
        if employee_id is not None:
            sql_checkEmployeeId="Select * from employees where employee_id = {}".format(employee_id)
            rows=this.db.run_query(sql_checkEmployeeId)
            if len(rows)==0:
                return {"error":"employee_id {} not found".format(employee_id)}
            where+=(" WHERE" if where is None else where+" AND")+(" employee_id='{}'".format(employee_id))
        
        #if type has been provided then check it is a valid value, returning an error if not or adding it to the sql query if it does 
        if type is not None:
            if type not in ["temperature","humidity","co2","ccon"]:
                return {"error","unknown type {}".format(type)}
            where+=(" WHERE" if where is None else where+" AND")+(" type='{}'".format(type))


        #retrieve the data from the database
        query+=where
        rows=this.db.run_query(query)


        #reformat the data so it has labels
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
        
        #check that max has a valid value
        if max not in [0,1]:
            return {"error": "max value {} not recognised, must be 0 or 1".format(max)}
        
        #check that the employee_id exists in the database
        sql_checkEmployeeId="""SELECT * FROM employees WHERE employee_id='{}'""".format(employee_id)
        rows=this.db.run_query(sql_checkEmployeeId)
        if len(rows)==0:
            return {"error":"unkown employee_id {}".format(employee_id)}

        #check that there isn't an alert with the exact same details already
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
        
        #get the device_id used by the database rather than the device_name used by the user and return an error if the device_name doesn't exist
        sqlGetDeviceId="SELECT device_id FROM devices WHERE device_name='{}'".format(device_name)
        rows=this.db.run_query(sqlGetDeviceId)
        if len(rows)==0:
            return {"error":"unrecognised device_name {}".format(device_name)}
        device_id=rows[0][0]

        #create the alert
        sqlCreateAlert="INSERT INTO alerts (employee_id, device_id, threshold, max) VALUES ('{}','{}','{}','{}')".format(employee_id,device_id,threshold,max)
        this.db.run_no_return(sqlCreateAlert)
        
        #make sure it can be found after creating
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"Alert Not found in database after insert"}
        
        #reformat the data so it has labels
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
        this.db.run_no_return(sqlUpdate)
        
        #get the updated data, and check that the device_id still exists in the database and hasn't been corrupted/lost
        sqlCheckExisting="""
SELECT alert_id, employee_id, device_name, type, threshold, max 
FROM alerts 
INNER JOIN devices
ON alerts.device_id=devices.device_id
WHERE alert_id='{}'""".format(alert_id)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"Alert not found in database after update"}
        
        #reformat the data so it has labels
        output=[]
        columns=["alert_id", "employee_id", "device_name", "type", "threshold", "max"]
        for each in rows:
            alert={}
            for i in range(len(columns)):
                alert[columns[i]]=each[i]
            
            output.append(alert)
            return {"message":"success", "updatedAlert": output}
        
    def removeAlerts(this,alert_id:int,auth:bool=True):
        if not auth:
            return {"error":"authorisation failed"}
        
        #check that the alert_id exists in the database
        sqlCheckExisting="SELECT * FROM alerts WHERE alert_id='{}'".format(alert_id)
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)==0:
            return {"error":"unrecognised alert_id {}".format(alert_id)}
        
        #delete the alert
        sqlRemove="DELETE FROM alerts WHERE alert_id = '{}'".format(alert_id)
        this.db.run_no_return(sqlRemove)
        
        #check that the alert no longer exists
        rows=this.db.run_query(sqlCheckExisting)
        if len(rows)!=0:
            return {"error":"alert with alert_id={} found in database after deletion".format(alert_id)}
        return {"message":"success"}