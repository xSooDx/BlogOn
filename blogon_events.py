import os
from datetime import datetime

event = ('post_create', 'post_update', 'post_delete', 'user_register')
logfile = "blogon.log"


def logEvent(eventName, eventData):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        log = open(logfile, 'a')
        log.write(date + "|" + eventName + "|" + eventData + "\n")
        log.close()
    except Exception as e:
        print("Logging Error || %s\n %s | %s - %s" % (str(e), date, eventName, eventData))


def checkLogTime():
    return os.path.getmtime(logfile)


def logTail(n=10):
    i = 0
    lines = []
    bytes_per_line = 100
    try:
        log = open(logfile, 'r')
        log.seek(0, 2)
        sz = log.tell()
        log.seek(max(sz - (bytes_per_line * n), 0), 0)
        for line in log:
            lines.append(line)
        lines = lines[:-(n + 1):-1]
    except Exception as e:
        pass

    return lines
