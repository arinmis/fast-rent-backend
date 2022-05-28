import datetime

def epochToDate(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%d-%m-%Y')
