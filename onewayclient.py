# https://beau.click/jsonrpc/websockets

from jsonrpcclient.clients.websockets_client import WebSocketsClient
import websockets
import asyncio
import json

from logging import getLogger, config
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


async def main():
    try:
        async with websockets.connect('ws://localhost:5000/jsonrpc') as websocket:
            logger.info("websocket connected. " + str(websocket))
            response = await WebSocketsClient(websocket).request('api.v1.echo', "hello!")
            logger.info("result: " + response.data.result)
            response = await WebSocketsClient(websocket).request('api.v1.shutdown')
        logger.info("websocket disconnected. " + str(websocket))
    except websockets.exceptions.ConnectionClosed:
        logger.info("websocket disconnected. " + str(websocket))
    except ConnectionRefusedError as ex:
        logger.info("websocket connection refused. " + ex.strerror)

if __name__ == '__main__':
    logger.info("started.")
    asyncio.get_event_loop().run_until_complete(main())
    logger.info("exit.")
