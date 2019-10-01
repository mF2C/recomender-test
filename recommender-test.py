import logging
import colorlog     # https://github.com/borntyping/python-colorlog
from os import environ

from flask import Flask, jsonify

from common.logs import LOG, DEBUG, INFO
from common.CIMI import CIMIcalls as CIMI

__status__ = 'Test'
__version__ = '1.0'

DEBUG_FLAG = environ.get('DEBUG', default='False') == 'True'
RECOMMENDER_PORT = int(environ.get('RECOMMENDER_PORT', default=46020))

# Set Logger
if DEBUG_FLAG:
    LOG.setLevel(DEBUG)
else:
    LOG.setLevel(INFO)


LOG.info('Recommender Test Module. Version {} Status {}'.format(__version__,__status__))

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/mf2c/optimal', methods=['POST'], strict_slashes=False)
def recommender_get_ips():
    topology = CIMI.get_topology()
    agent_res, res_id = CIMI.getAgentResource()
    if res_id != '' and 'device_ip' in agent_res:
        self_device_ip = agent_res['device_ip']
    else:
        self_device_ip = None
    response = [{'ipaddress': ip[1]} for ip in topology]
    if self_device_ip is not None:
        response.append({'ipaddress': self_device_ip})
    LOG.debug('Recommender API response: \"{}\"'.format(response))
    return jsonify(response), 200


def main():
    app.run(debug=DEBUG_FLAG, host='0.0.0.0', port=RECOMMENDER_PORT)


if __name__ == '__main__':
    main()
    exit(0)
