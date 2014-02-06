# -*- coding: utf-8 -*-
import csv
import pandas as pd
import datetime


class DateParser(object):
    pass


def parseLog(filename):
    awake = True
    # these are intended to have days as keys, with each value therein
    #    being a pandas Series instance; each index is the start time;
    #    each value is the duration
    awakeTimes = {}
    leftFeeds = {}
    rightFeeds = {}
    diaperTimes = {}

    with open(filename) as log:
        reader = csv.reader(log)
        reader.next()
        line = reader.next()
        if line[2] == "down":
            line = reader.next()
        uptime = line[0]+ " "+ line[1]
        for i, line in enumerate(reader):
            if line[2] == "down":
                downtime = line[0]+" "+line[1]
                awakeTimes[uptime]=timeDiffsToTimeDelta(uptime, downtime)
            elif line[2] == "up":
                uptime = line[0]+ " "+ line[1]
            if len(line[3]) > 1:
                leftFeeds[line[0] + " " + line[3][:line[3].find("-")]] = \
                    timeDiffStringToTimeDelta(line[3])
            if len(line[4]) > 1:
                rightFeeds[line[0] + " " + line[4][:line[4].find("-")]] = \
                    timeDiffStringToTimeDelta(line[4])
        leftFeeds = pd.Series(leftFeeds)
        rightFeeds = pd.Series(rightFeeds)
        awakeTimes = pd.Series(awakeTimes)
    return awakeTimes, leftFeeds, rightFeeds

def timeDiffsToTimeDelta(time1, time2):
    time1 = parseDateStringToDateTime(time1)
    time2 = parseDateStringToDateTime(time2)
    return time2-time1
    
def parseDateStringToDateTime(string):
    slash = string.find("/")
    month = int(string[:slash])
    string = string[slash+1:]
    slash = string.find("/")
    day = int(string[:slash])
    space = string.find(" ")
    year = int(string[slash+1:space])
    string = string[space+1:]
    colon = string.find(":")
    hour = int(string[:colon])
    minute = int(string[colon+1:colon+3])
    return datetime.datetime(year, month, day, hour, minute)

def timeDiffStringToTimeDelta(timeDiff):
    # parse the string into its distinct times
    a, b = timeDiff.split("-")
    # exact date doesn't matter here, only the relative time.  Choose arbitrary
    #    date to use as datetime
    date = datetime.datetime(2014, 1, 1)
    acolon=a.find(":")
    a = date + datetime.timedelta(hours=int(a[:acolon]), 
                                  minutes=int(a[acolon+1:]))
    bcolon=b.find(":")
    b = date + datetime.timedelta(hours=int(b[:bcolon]), 
                                  minutes=int(b[bcolon+1:]))
    if b < a:
        b += datetime.timedelta(days=1)
    return b - a

# views:
# hours of sleep per day
# bar chart of sleep (blue) vs awake (red) - several days shown; each as bar
#

if __name__ == "__main__":
    import sys
    a, l, r = parseLog(sys.argv[1])
    print a
    print l
    print r
