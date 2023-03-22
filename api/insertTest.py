from dbConnect import *

db=dbConnect()

result=db.run_query("select * from devices")
for each in result:
    print(each)

db.run_insert('INSERT INTO devices (type,show,device_name,product_number) VALUES ("{}",{},"{}",{})'.format("test",0,"testName",0)) 

result=db.run_query("select * from devices")
for each in result:
    print(each)