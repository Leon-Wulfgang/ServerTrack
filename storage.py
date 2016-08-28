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

    # init dictionary of records
    def __init__(self):
        self.data = {}

    # insert record to data
    def insert(self, serverLoad):
        sid = serverLoad['serverId']

        # current time interval = timestamp / 60 , each minute
        timeinterval = int(time.time() / 60)

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

        # current time interval = timestamp / 60 , each minute
        timeinterval = int(time.time() / 60)

        cpuAverage = sum(serverLoadInfo['cpu'][timeinterval]) / len(serverLoadInfo['cpu'][timeinterval])
        ramAverage = sum(serverLoadInfo['ram'][timeinterval]) / len(serverLoadInfo['ram'][timeinterval])

        return {
            'serverName': serverLoadInfo['name'],
            'cpuAverage': cpuAverage,
            'ramAverage': ramAverage,
        }

