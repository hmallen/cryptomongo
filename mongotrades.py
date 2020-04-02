import asyncio
import configparser
#from decimal import Decimal
from bson.decimal128 import Decimal128 as Decimal
import functools
#import json
import simplejson as json
import logging
from pprint import pprint
import signal
import sys

from pymongo import MongoClient

import websockets
from websockets import WebSocketClientProtocol

config_path = 'config/settings.conf'
config = configparser.ConfigParser()
config.read(config_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


## Standard Functions ##

def build_subscription(market_list):
    markets = [
        {"streamSubscription": {"resource": f"markets:{mkt.strip(' ')}:trades"}} \
        for mkt in market_list.split(',')]
    
    constructed_message = {'subscribe': {'subscriptions': markets}}

    return constructed_message


def format_message(message):
    if 'marketUpdate' in message:
        for item in message['marketUpdate']['market']:
            message['marketUpdate']['market'][item] = int(
                message['marketUpdate']['market'][item])
        
        trades_converted = []
        for trade in message['marketUpdate']['tradesUpdate']['trades']:
            trade_reformatted = dict(
                amount=Decimal(trade['amountStr']),
                # externalId=trade['externalId'],
                orderSide=trade['orderSide'],
                price=Decimal(trade['priceStr']),
                timestamp=int(trade['timestamp']),
                timestampNano=int(trade['timestampNano'])
            )
            trades_converted.append(trade_reformatted)
        
        message['marketUpdate']['tradesUpdate']['trades'] = trades_converted
    
    pprint(message)

    return message


def signal_exit(signame, loop):
    print("Got signal %s: exit" % signame)
    loop.stop()


## AsyncIO Functions ##

async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    mongo_client = MongoClient(
        f"mongodb://{config['mongodb']['host']}:{config['mongodb']['port']}/")
    trade_collection = mongo_client[
        config['mongodb']['database']][config['mongodb']['collection']]
    
    async for message in websocket:
        message_json = format_message(json.loads(message))
        # pprint(message_json)

        doc_id = trade_collection.insert_one(message_json).inserted_id
        logger.debug('doc_id: {}'.format(doc_id))


async def consume(api_key: str, sub_msg: str) -> None:
    websocket_resource_url = f'wss://stream.cryptowat.ch/connect?apikey={api_key}'
    async with websockets.connect(websocket_resource_url) as websocket:
        await websocket.send(json.dumps(sub_msg))
        await consumer_handler(websocket)


if __name__ == '__main__':
    subscription_message = build_subscription(config['cryptowatch']['market_ids'])
    
    loop = asyncio.get_event_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(signal_exit, signame, loop))
    
    try:
        loop.run_until_complete(
            consume(api_key=config['cryptowatch']['api'], sub_msg=subscription_message))
    finally:
        loop.close()