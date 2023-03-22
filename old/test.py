each = "macAddress:A3:68:12:B4:98:45,ipAddress:192.0.2.1,errors:[code:404;message:not found]"
value=each.split(",")
print(value)
macAddress=value[0].split(":",1)[1]
ipAddress=value[1].split(":",1)[1]
errors=value[2].split(":",1)[1].split("[")[1].split("]")[0].split(";")
errorCode=errors[0].split(":",1)[1]
errorMessage=errors[1].split(":",1)[1]
print(macAddress)
print(ipAddress)
print(errors)
print(errorCode)
print(errorMessage)