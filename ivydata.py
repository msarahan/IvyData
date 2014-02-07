# -*- coding: utf-8 -*-
import csv
import pandas as pd
import datetime

import matplotlib.pyplot as plt

class DateParser(object):
    def __init__(self, filename):
        super(DateParser, self).__init__()
        self.parseLog(filename)
        self.print_stats()

    def print_stats(self):
        print self.awakeTimes
        print self.leftFeeds
        print self.rightFeeds

    def plot_feeds(self, date_range):
        fig, axes = plt.subplots(1, 3)
        # collect data from within date range
        # group by day
        # plot one bar per day
            # for bars that extend beyond end of day,
            #    keep tally of remainder, start next day with bar at 0,
            #    extending to remainder
        axes[0].broken_bar([])

    def parseLog(self, filename):
        # these are intended to have days as keys, with each value therein
        #    being a pandas Series instance; each index is the start time;
        #    each value is the duration
        awakeTimes = {}
        leftFeeds = {}
        rightFeeds = {}
        diaperTimes = {}

        with open(filename) as log:
            reader = csv.reader(log)
            # the first line has headers.  Skip it.
            reader.next()
            # read the first data line
            line = reader.next()
            # we want to start with an "up" time, because we use that as our
            #    frame of reference.  Skip the first data line if it is a
            #    downer.
            if line[2] == "down":
                line = reader.next()
            # store a datetime representing the time that she woke up
            uptime = self.parseDateStringToDateTime(line[0] + " " + line[1])
            # Loop over the lines of the file
            for i, line in enumerate(reader):
                # if she went to sleep, record the total time she's been awake
                if line[2] == "down":
                    downtime = self.parseDateStringToDateTime(line[0] + " " +
                                                              line[1])
                    awakeTimes[uptime] = (downtime - uptime).seconds / 3600.0
                # if she woke up, establish a new frame of reference
                elif line[2] == "up":
                    uptime = self.parseDateStringToDateTime(line[0] + " " +
                                                            line[1])
                # if we have a feeding record on this line for the left breast,
                #    store it as the time started, with total time fed
                if len(line[3]) > 1:
                    time = self.parseDateStringToDateTime(line[0] + " " +
                        line[3][:line[3].find("-")])
                    leftFeeds[time] = \
                        self.timeDiffStringToTimeDelta(line[3])
                # if we have a feeding record on this line for the right
                #   breast, store it as the time started, with total time fed
                if len(line[4]) > 1:
                    time = self.parseDateStringToDateTime(line[0] + " " +
                                        line[4][:line[4].find("-")])
                    rightFeeds[time] = \
                        self.timeDiffStringToTimeDelta(line[4])
        # convert the read-out dictionaries into Pandas Series objects for
        #     further manipulation and display
        self.leftFeeds = pd.Series(leftFeeds)
        self.rightFeeds = pd.Series(rightFeeds)
        self.awakeTimes = pd.Series(awakeTimes)

    def timeDiffsToTimeDelta(self, time1, time2):
        time1 = self.parseDateStringToDateTime(time1)
        time2 = self.parseDateStringToDateTime(time2)
        return time2 - time1

    def parseDateStringToDateTime(self, string):
        slash = string.find("/")
        month = int(string[:slash])
        string = string[slash + 1:]
        slash = string.find("/")
        day = int(string[:slash])
        space = string.find(" ")
        year = int(string[slash + 1:space])
        string = string[space + 1:]
        colon = string.find(":")
        hour = int(string[:colon])
        minute = int(string[colon + 1:colon + 3])
        return datetime.datetime(year, month, day, hour, minute)

    def timeDiffStringToTimeDelta(self, timeDiff):
        # parse the string into its distinct times
        a, b = timeDiff.split("-")
        # exact date doesn't matter here, only the relative time.  Choose arbitrary
        #    date to use as datetime
        date = datetime.datetime(2014, 1, 1)
        acolon = a.find(":")
        a = date + datetime.timedelta(hours=int(a[:acolon]),
                                      minutes=int(a[acolon + 1:]))
        bcolon = b.find(":")
        b = date + datetime.timedelta(hours=int(b[:bcolon]),
                                      minutes=int(b[bcolon + 1:]))
        if b < a:
            b += datetime.timedelta(days=1)
        return (b - a).seconds / 3600.0

# views:
# hours of sleep per day
# bar chart of sleep (blue) vs awake (red) - several days shown; each as bar
#

if __name__ == "__main__":
    import sys
    parser = DateParser(sys.argv[1])
