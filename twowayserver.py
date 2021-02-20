# https://pypi.org/project/wsjsonrpc/

import sys
import threading
import time
import json

from twisted import logger
from twisted.internet import defer
from twisted.internet import reactor

from wsjsonrpc import factory

from logging import getLogger, config
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


@defer.inlineCallbacks
def _ping(protocol, string):
    logger.info("called " + string)
    result = yield protocol.request("api.v1.pong", {"string": string + " ping"})
    return result


def shutdownCore():
    time.sleep(1)
    reactor.stop()


def _shutdown(protocol):
    logger.info("called")
    threading.Thread(target=shutdownCore).start()
    return


def main():
    logger.info("started.")
    serverFactory = factory.JsonRpcWebSocketServerFactory(
        "ws://localhost:5000/jsonrpc")

    serverFactory.registerMethod("api.v1.ping", _ping)
    serverFactory.registerMethod("api.v1.shutdown", _shutdown)

    reactor.listenTCP(5000, serverFactory)
    reactor.run()
    logger.info("exit.")


if __name__ == "__main__":
    main()
