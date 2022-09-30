from .vechain import make_call, make_transact
from src.extensions import redis_cluster
from src.constants import AppConstants
from src.config import DefaultConfig


class Token:
    def __init__(self, _address):
        self.address = _address

    def get_symbol(self):
        return make_call(
                contract_address=self.address,
                abi_file_name="VIP180",
                call_function_name="symbol",
                params=[]
            )['0']

    def get_decimals(self):
        return make_call(
                contract_address=self.address,
                abi_file_name="VIP180",
                call_function_name="decimals",
                params=[]
            )['0']

    @staticmethod
    def verify_symbol(_symbol):
        if _symbol.startswith("W"):
            return _symbol[1:]
        else:
            return _symbol

    def get_price(self):
        _symbol = self.get_symbol()
        _symbol = self.verify_symbol(_symbol)
        return make_call(
                contract_address=redis_cluster.hget(
                    name=AppConstants.gen_redis_hash_for_env(DefaultConfig.ENV),
                    key=f"SEER_{_symbol}USD"
                ),
                abi_file_name="SeerOracle",
                call_function_name="latestAnswer",
                params=[]
            )['0']


