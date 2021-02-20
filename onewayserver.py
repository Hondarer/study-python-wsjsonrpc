# https://beau.click/jsonrpc/websockets

from jsonrpcserver import method, async_dispatch as dispatch
import websockets
import asyncio
import json

from logging import getLogger, config
with open('log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


@method(name="api.v1.echo")
async def echo(args):
    logger.info("echo: " + args)
    return args


@method(name="api.v1.shutdown")
async def exit():
    logger.info("shutdown request was recieved.")
    asyncio.get_event_loop().stop()
    return


async def main(websocket, path):
    logger.info("websocket connected. " + str(websocket))
    while True:
        try:
            recvValue = await websocket.recv()
            response = await dispatch(recvValue)
            if response.wanted:
                await websocket.send(str(response))
        except websockets.exceptions.ConnectionClosed:
            logger.info("websocket disconnected. " + str(websocket))
            break

if __name__ == '__main__':
    logger.info("started.")
    start_server = websockets.serve(main, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    logger.info("websocket JSON-RPC server was started.")
    asyncio.get_event_loop().run_forever()
    logger.info("exit.")
