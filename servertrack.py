"""
ReSTful API server for responding and storing incoming records
    with support of microFramework Flask (http://flask.pocoo.org)
"""

from flask import Flask, request, jsonify
from storage import Storage

# init flask app
app = Flask(__name__)

# init storage
storage = Storage()


@app.route("/record", methods=['POST'])
def serverListResource():
    """
    resource for list of server loads
    """
    if request.method == 'POST':
        serverId = request.args.get('sid', '')
        serverName = request.args.get('name', '')
        cpuLoad = request.args.get('cpu', '')
        ramLoad = request.args.get('ram', '')
        return recordLoad(serverId, serverName, cpuLoad, ramLoad)


@app.route("/record/<int:sid>/<string:interval>", methods=['GET'])
def serverDetailResource(sid, interval):
    """
    resource for server load detail
    """
    if request.method == 'GET':
        return getLoad(sid, interval)


# store POST record
def recordLoad(serverId, serverName, cpuLoad=None, ramLoad=None):
    serverLoad = {
        'serverId': int(serverId),
        'serverName': str(serverName),
        'cpuLoad': float(cpuLoad),
        'ramLoad': float(ramLoad),
    }
    storage.insert(serverLoad)
    result = serverLoad
    return jsonify(result)


# GET server stat by id & type
def getLoad(sid, interval='m'):
    result = storage.getLoadBySidInterval(sid, interval)
    return jsonify(result)


"""
main
"""
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
