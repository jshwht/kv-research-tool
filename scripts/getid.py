import datetime

def getid():
    dt = str(datetime.datetime.now())
    return(dt[0:4]+dt[5:7]+dt[8:10]+dt[11:13]+dt[14:16]+dt[17:19])