from .vechain import make_call
from pydash import get


class PoolPair:
    def __init__(self, _address):
        self.address = _address

    def get_decimals(self):
        return make_call(
                contract_address=self.address,
                abi_file_name="PoolPair",
                call_function_name="decimals",
                params=[]
            )['0']

    def get_token(self, _token_name):
        return make_call(
                contract_address=self.address,
                abi_file_name="PoolPair",
                call_function_name=_token_name,
                params=[]
            )['0']

    def get_total_lp(self):
        return make_call(
                contract_address=self.address,
                abi_file_name="PoolPair",
                call_function_name="totalSupply",
                params=[]
            )['0']

    def get_reserves(self):
        _reserves = make_call(
                contract_address=self.address,
                abi_file_name="PoolPair",
                call_function_name="getReserves",
                params=[]
            )
        return get(_reserves, "_reserve0"), get(_reserves, "_reserve1")
