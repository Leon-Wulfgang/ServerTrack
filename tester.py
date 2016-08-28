import httplib2
import json
import random

# API address
address = 'http://localhost:5000'


# POST a random load record
def postRandomLoad():

    cpu = random.random()
    ram = random.random()

    url = address + "/record?id=01&name=hello&cpu=%s&ram=%s" % (cpu, ram)
    h = httplib2.Http()
    resp, result = h.request(url, 'POST')
    if resp['status'] != '200':
        print resp, result


def getLoadStatus():
    sid = '01'
    interval = 'm'
    url = address + "/record/%s/%s" % (sid, interval)
    h = httplib2.Http()
    resp, result = h.request(url, 'GET')
    if resp['status'] != '200':
        print resp
    print result


if __name__ == '__main__':
    postRandomLoad()
    getLoadStatus()
