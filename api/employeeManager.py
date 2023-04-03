from api.dbConnect import *

class employeeManager:
    def __init__(this):
        this.db=dbConnect()

    def getEmployees(this,auth:bool=True,employee_ids:list[int]=None):
        if not auth:
            return {"error":"authorisation failed"}
        where:str=None
        query="SELECT employee_id, username, password, email, first_name, last_name FROM employees"
        
        #if employee_ids have been provided, then add them to the sql query
        if employee_ids is not None:
            where=" WHERE  employee_id IN ('{}'".format(employee_ids[0])
            for i in range(1,len(employee_ids)):
                where += ",'{}'".format(employee_ids[i])
            where+=")"
        if where is not None:
            query+=where
        rows=this.db.run_query(query)
        output=[]
        
        #reformat the data so it has labels
        columns=["employee_id", "username", "password", "email", "first_name","last_name"]
        for each in rows:
            employee={}
            for i in range(len(columns)):
                employee[columns[i]]=each[i]
            output.append(employee)
        return {"message":"success","employees":output}