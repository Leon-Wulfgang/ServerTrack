"""
class Storage for storing incoming records
"""
import time


class Storage(object):
    """
    data structure for record storage
    root: {
        server_id:{
            name:
            cpu:{
                timeinterval : timestamp / 60
            }
            ram:{
                timeinterval : timestamp / 60
            }
        }
    }
    """
    data = None
    lastPurgeTime = None
    SECOND_IN_MINUTE = 60
    PAST_HOUR = 60
    PAST_DAY = 1440

    # init dictionary of records
    def __init__(self):
        self.data = {}

    # insert record to data
    def insert(self, serverLoad):
        # check to see if a purge is needed
        self.purgeOld()

        # server id
        sid = serverLoad['serverId']

        # current time interval = timestamp / SECOND_IN_MINUTE , each minute
        currentTime = time.time()
        if 'ts' in serverLoad:
            currentTime = float(serverLoad['ts'])
        timeinterval = int(currentTime / self.SECOND_IN_MINUTE)


        # create record for server id if not exist
        if sid not in self.data:
            self.data[sid] = {
                'name': serverLoad['serverName'],
                'cpu': {},
                'ram': {},
            }

        # insert record for time interval
        if timeinterval not in self.data[sid]['cpu']:
            self.data[sid]['cpu'][timeinterval] = []
        if timeinterval not in self.data[sid]['ram']:
            self.data[sid]['ram'][timeinterval] = []

        # insert record cpu and ram
        self.data[sid]['cpu'][timeinterval].append(serverLoad['cpuLoad'])
        self.data[sid]['ram'][timeinterval].append(serverLoad['ramLoad'])

    # return load status by sid & interval type
    def getLoadBySidInterval(self, sid, interval='m'):
        serverLoadInfo = self.data[sid]
        result = {}
        result['serverName'] = serverLoadInfo['name']
        if interval == 'm':
            data = self.getPast(serverLoadInfo, self.PAST_HOUR)
            formatData = {
                'cpu': {},
                'ram': {},
            }
            # format data
            for interval in data['cpu']:
                formatData['cpu'][time.strftime("%m/%d %H:%M", time.localtime(interval * self.SECOND_IN_MINUTE))] = data['cpu'][interval]
            for interval in data['ram']:
                formatData['ram'][time.strftime("%m/%d %H:%M", time.localtime(interval * self.SECOND_IN_MINUTE))] = data['ram'][interval]
            result['data'] = formatData

        elif interval == 'h':
            data = self.getPast(serverLoadInfo, self.PAST_DAY)
            formatData = {
                'cpu': {},
                'ram': {},
            }

            # sort cpu intervals
            cpuIntervals = sorted(data['cpu'].keys())
            lastInterval = cpuIntervals[0]
            for interval in cpuIntervals:
                # make last interval the hour basket
                intervalHour = time.strftime("%m/%d %H:00", time.localtime(lastInterval * self.SECOND_IN_MINUTE))
                # within this hour, put data in basket
                if interval < lastInterval + self.PAST_HOUR:
                    if intervalHour not in formatData['cpu']:
                        formatData['cpu'][intervalHour] = []
                    formatData['cpu'][intervalHour].append(data['cpu'][interval])
                # new hour
                else:
                    # init helpers
                    lastInterval = interval

            # calculate averages
            for hour in formatData['cpu']:
                formatData['cpu'][hour] = avg(formatData['cpu'][hour])

            # sort ram intervals
            ramIntervals = sorted(data['ram'].keys())
            lastInterval = ramIntervals[0]
            for interval in ramIntervals:
                # make last interval the hour basket
                intervalHour = time.strftime("%m/%d %H:00", time.localtime(lastInterval * self.SECOND_IN_MINUTE))
                # within this hour, put data in basket
                if interval < lastInterval + self.PAST_HOUR:
                    if intervalHour not in formatData['ram']:
                        formatData['ram'][intervalHour] = []
                    formatData['ram'][intervalHour].append(data['ram'][interval])
                else:
                    # init helpers
                    lastInterval = interval

            # calculate averages
            for hour in formatData['ram']:
                formatData['ram'][hour] = avg(formatData['ram'][hour])

            result['data'] = formatData

        # debug
        # result['debug'] = self.getDebugInfo(serverLoadInfo)

        return result

    # get past average load for a given interval of time range
    def getPast(self, serverLoadInfo, pastInterval=PAST_HOUR):
        cpu, ram = {}, {}
        currentTimeInterval = int(time.time() / self.SECOND_IN_MINUTE)
        endTimeInterval = currentTimeInterval - pastInterval
        while currentTimeInterval > endTimeInterval:
            if currentTimeInterval in serverLoadInfo['cpu']:
                cpu[currentTimeInterval] = avg(serverLoadInfo['cpu'][currentTimeInterval])
            if currentTimeInterval in serverLoadInfo['ram']:
                ram[currentTimeInterval] = avg(serverLoadInfo['ram'][currentTimeInterval])
            currentTimeInterval -= 1
        return {
            'cpu': cpu,
            'ram': ram,
        }

    # purge old data, if data is older than self.PAST_DAY, delete node
    def purgeOld(self):
        # check last purge time
        if self.lastPurgeTime < (time.time() - self.SECOND_IN_MINUTE*self.PAST_DAY*self.PAST_HOUR):

            for server in self.data:
                for interval in server['cpu']:
                    if interval < time.time() - self.PAST_DAY:
                        del interval
                for interval in server['ram']:
                    if interval < time.time() - self.PAST_DAY:
                        del interval

            self.lastPurgeTime = time.time()

    def getDebugInfo(self, serverLoadInfo):
        # current time interval = timestamp / 60 , each minute
        timeinterval = int(time.time() / self.SECOND_IN_MINUTE)

        # debug
        debugCountInterval = len(serverLoadInfo['cpu'])
        debugIntervalKeys = serverLoadInfo['cpu'].keys()
        debugCountEntry = len(serverLoadInfo['cpu'][timeinterval])
        debug = {
            'debugCountInterval': debugCountInterval,
            'debugCountEntry': debugCountEntry,
            'debugCountKeys': debugIntervalKeys,
        }
        return debug



def avg(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
