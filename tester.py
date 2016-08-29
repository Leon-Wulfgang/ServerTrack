import httplib2
import random
import time

# CONFIGS ####################################
address = 'http://localhost:5000'
runtime = 10
serverId = 1
# END CONFIGS ################################


# POST a random load record
def postRandomLoad(sid, name):

    cpu = random.random()
    ram = random.random()

    url = address + "/record?sid=%s&name=%s&cpu=%s&ram=%s" % (sid, name, cpu, ram)
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
    endTime = time.clock() + runtime
    print "Populating server data for %s seconds " % runtime
    while time.clock() < endTime:
        postRandomLoad(serverId, 'helloServer')

    print "GET server status for server ID: %s for the past hour break down by minute" % serverId
    getLoadStatus(serverId, 'm')
    print "GET server status for server ID: %s for the past day break down by hour" % serverId
    getLoadStatus(serverId, 'h')


