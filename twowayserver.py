# https://pypi.org/project/wsjsonrpc/

import sys
import threading
import time
import json

from twisted.internet import defer
from twisted.internet import reactor

import wsjsonrpc

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
    reactor.stop()


def _shutdown(protocol):
    logger.info("called.")
    reactor.callLater(0.1, shutdownCore)
    return


def main():
    logger.info("started.")
    serverFactory = wsjsonrpc.factory.JsonRpcWebSocketServerFactory(
        "ws://localhost:5000/jsonrpc")

    serverFactory.registerMethod("api.v1.ping", _ping)
    serverFactory.registerMethod("api.v1.shutdown", _shutdown)

    reactor.listenTCP(5000, serverFactory)
    reactor.run()
    logger.info("will exit.")


if __name__ == "__main__":
    main()
