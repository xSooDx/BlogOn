from functools import wraps
from datetime import datetime

event = ('post_create', 'post_update', 'post_delete', 'user_register')
logfile = "blogon.log"


def logEvent(eventName, eventData):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        log = open(logfile, 'a')
        log.write(date + " : " + eventName + " - " + eventData + "\n")
        log.close()
    except Exception as e:
        print("Logging Error :: %s\n %s : %s - %s" % (str(e), date, eventName, eventData))
