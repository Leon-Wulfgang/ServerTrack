import httplib2
import random
import time

# CONFIGS ####################################
address = 'http://localhost:5000'   # server address
runtime = 10                        # run POST continuously for X seconds
serverId = 1                        # the server ID that POSTs to the server
pastHourCount = 24                  # X hours in the past will be populated with data
pastHourData = 10                   # X entries will be POSTed for each hour in the past
# END CONFIGS ################################


# POST a random load record
def postRandomLoad(sid, name, ts=None):

    cpu = random.random()
    ram = random.random()

    url = address + "/record?sid=%s&name=%s&cpu=%s&ram=%s" % (sid, name, cpu, ram)
    if ts:
        url = "%s&ts=%s" % (url, ts)

    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        print resp, result


# GET server status by server id & interval type
def getLoadStatus(sid, interval):
    url = address + "/record/%s/%s" % (sid, interval)
    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        print resp
    print result


if __name__ == '__main__':
    startTime = time.clock()

    print "Populating server data for past %s hours " % pastHourCount
    for i in range(1, pastHourCount+1):
        for j in range(1, pastHourData+1):
            postRandomLoad(serverId, 'helloServer', time.time() - i*60*60 + j*60)

    endTime = time.clock() + runtime
    print "Populating server data for %s seconds " % runtime
    while time.clock() < endTime:
        postRandomLoad(serverId, 'helloServer')

    print "GET server status for server ID: %s for the past hour break down by minute" % serverId
    getLoadStatus(serverId, 'm')

    print "GET server status for server ID: %s for the past day break down by hour" % serverId
    getLoadStatus(serverId, 'h')

    print "Time elapsed:", time.clock()-startTime

