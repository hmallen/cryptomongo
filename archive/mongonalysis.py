import configparser
import logging
import sys

from pymongo import MongoClient

config_path = 'config/settings.conf'
config = configparser.ConfigParser()
config.read(config_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradeAnalyzer:

    def __init__(self):
        self.mongo_client = MongoClient(
            f"mongodb://{config['mongodb']['host']}:{config['mongodb']['port']}/")
        
        self.trade_collection = mongo_client[
            config['mongodb']['database']][config['mongodb']['collection']]


if __name__ == '__main__':
    print(f"Selected collection \"{config['mongodb']['collection']}\" in database \"{config['mongodb']['database']}\" for analysis.\n")

    user_selection = input('Is this correct? [Y/n]\n')

    if user_selection.lower() == 'y' or user_selection == '':
        print('Trade collection confirmed. Beginning analysis.')
    
    elif user_selection.lower() == 'n':
        print('User cancelled analysis. Exiting.')
        sys.exit()

    else:
        print('Unrecognized input. Exiting.')
        sys.exit(1)

    analyze = TradeAnalyzer()