"""
Cronjobs run like clockwork, and sometimes you want something to
happen a little less predictably. The Scheduler class will schedule
events to happen according to a normal distribution.

You specify the mean of the normal distribution (how often something
should happen, on average) and the standard deviation (how much
reality is allowed to deviate from the average).

So if you want something to happen every hour, more or less, you can
run your cronjob once every ten minutes and have it call this code to
check whether anything should actually happen:

Scheduler(60*60,60*10).is_it_time(last_time_something_happened)

Since you're buying a brand new lottery ticket every time you call
is_it_time(), events will actually happen more often than you schedule
them for. You can compensate for this by setting your mean a little
higher than you want to.
"""

from datetime import datetime
import os
import random
import time

class Scheduler(object):

    """
    scheduler = Scheduler(mean=60*60*4, stdev=60*1)
    print scheduler.is_it_time(scheduler.file_mtime("last_update"))
    """

    def __init__(self, mean, stdev):
        self.mean = mean
        self.stdev = stdev

    def file_mtime(self, path):
        mtime = os.stat(path).st_mtime
        return datetime.fromtimestamp(mtime)

    def is_it_time(self, last_time):
        return self._is_it_time(last_time, datetime.now())

    def is_it_time_utc(self, last_time):
        return self._is_it_time(last_time, datetime.utcnow())

    def _is_it_time(self, last_time, now):
        difference = now - last_time
        choice = random.gauss(self.mean, self.stdev)
        return difference.seconds > choice


