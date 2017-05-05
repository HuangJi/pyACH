import json
import random
import plyvel

from pymongo import MongoClient
from config import BANK_LIST, API_SMART_CONTRACT_TX_DB_PATH, API_SETTLE_TX_DB_PATH


class HistoryTx(object):
    db_url = 'mongodb://ach:graduate@ach.csie.org:27017/ach'
    db_name = 'ach'
    collection_name = 'transactions'

    def __init__(self):
        mongo = MongoClient(self.db_url)
        self.db = mongo[self.db_name]
        self.collection = self.db[self.collection_name]

    def get_query_dict(self, start_date, end_date):
        return {
            '$or': [
                {
                    'P_TDATE': end_date
                },
                {
                    'P_TDATE': start_date,
                    'P_TYPE': 'N'
                }
            ]
        }

    def get_random_data(self, tx_type):
        return {
            'P_PBANK': BANK_LIST[random.randint(0, len(BANK_LIST))],
            'P_RBANK': BANK_LIST[random.randint(0, len(BANK_LIST))],
            'P_TXTYPE': tx_type,
            'P_AMT': random.randint(0, 10) * 1000
        }

    def get_range_data_cursor(self, start_date, end_date):
        query = self.get_query_dict(start_date, end_date)
        cursor = self.collection.find(query, no_cursor_timeout=True)
        return cursor


class AbstractTx(object):
    """
    trigger_bank, receive_bank, type, amount, status, created_time,
    tx_id(gcoin)
    """
    def __init__(self):
        self.db = plyvel.DB(self.get_db_path(), create_if_missing=True)

    def get_db_path(self):
        if hasattr(self, 'db_path'):
            return getattr(self, 'db_path')
        else:
            raise AttributeError('`{}` attribute should be defined'.format('db_path'))

    def put_tx(self, key, tx):
        self.db.put(key, json.dumps(tx))


class SettleTx(AbstractTx):
    db_path = API_SETTLE_TX_DB_PATH


class SmartContractTx(AbstractTx):
    db_path = API_SMART_CONTRACT_TX_DB_PATH
