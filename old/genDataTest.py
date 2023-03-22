import random

def changeAndRound(data:float,maxChange:int,lowerBound:float,upperBound:float,decimalPlaceChange:int=0,roundTo:int=0) -> float: 
    """
    Make a random change to a float and return the result

    :param float data: The data to operate upon
    :param int maxChange: The maximum amount of change in one step in whole numbers
    :param float lowerBound: The lowest number the data can be
    :param float upperBound: The highest number the data can be
    :param int decimalPlaceChange: To how many decimal places can the data be changed default 0
    :param int roundTo: How many decimal places should the data be rounded to after changing default 0
    :return: The changed data
    :rtype: float
    """
    dpcScalar=pow(10,decimalPlaceChange)
    output=data+random.randint(-maxChange*dpcScalar,maxChange*dpcScalar)/(dpcScalar)
    if output<lowerBound:
        output=lowerBound
    elif output>upperBound:
        output=upperBound
    output=round(output,roundTo)
    return output

dataList=[50,50,50,50]
for i in range(0,100):
    for j in range(len(dataList)):
        dataList[j]=changeAndRound(dataList[j],10,100,10,5,)
    print(dataList)