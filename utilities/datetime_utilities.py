import datetime
import time
import os

def file_creation_date(file):
    creation_datetime = os.path.getctime(file)
    ceation_time = time.ctime(creation_datetime)
    tobj =time.strptime(ceation_time)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S',tobj)
    return timestamp
