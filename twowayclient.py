# https://pypi.org/project/wsjsonrpc/

import sys
import time
import json

from twisted import logger
from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor

from wsjsonrpc import factory, exception

from logging import getLogger, config
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


def _pong(protocol, string):
    logger.info("called " + string)
    result = string + " pong"
    return result


def getClientFactory(protocol="ws", hostname="localhost", port=8095, path="jsonrpcws"):
    if (protocol, port) in (("ws", 80), ("wss", 443)):
        url = "{}://{}:{}/{}".format(protocol, hostname, path.lstrip("/"))
    else:
        url = "{}://{}:{}/{}".format(protocol,
                                      hostname, port, path.lstrip("/"))

    clientFactory = factory.JsonRpcWebSocketClientFactory(url)

    if protocol == "ws":
        reactor.connectTCP(hostname, port, clientFactory)
    elif protocol == "wss":
        reactor.connectSSL(hostname, port, clientFactory)

    return clientFactory


@defer.inlineCallbacks
def main(reactor):
    logger.info("started.")

    clientFactory = getClientFactory(
        hostname="localhost", port=5000, path="jsonrpc")

    clientFactory.registerMethod("api.v1.pong", _pong)

    protocol = yield clientFactory.getProtocol()

    result = yield protocol.request("api.v1.ping", {"string": "hello!!"})
    logger.info("result: {}".format(result))

    yield protocol.request("api.v1.shutdown")
    logger.info("exit.")


if __name__ == "__main__":
    task.react(main)
