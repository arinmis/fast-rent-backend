import datetime

def epochToDate(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')
