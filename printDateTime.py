import datetime

now=datetime.datetime.now()
then="2021-05-16T08:13:15.361624Z"
timeFormat="%Y-%m-%dT%H:%M:%S.%fZ"
print(now)
print(datetime.datetime.strftime(now,timeFormat))
print(then)
print(datetime.datetime.strptime(then,timeFormat))
print(datetime.datetime.now()-datetime.timedelta(hours = 24))