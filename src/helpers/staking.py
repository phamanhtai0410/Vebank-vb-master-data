from .vechain import make_call, make_transact
from .token import Token
from .pool_pair import PoolPair
from src.constants import AppConstants
from src.models.staking_apr import StakingAPRModel
from src.models.staking_total import StakingTotalModel
from src.config import DefaultConfig


class Staking:
    def __init__(self, _staking_contract, _staked_token, _rewards_token, _is_lp=False):
        self.staking_contract = _staking_contract
        self.staked_token = _staked_token
        self.rewards_token = _rewards_token
        self.is_LP = _is_lp

    def get_total_staked(self):
        return make_call(
            contract_address=self.staked_token,
            abi_file_name="VIP180",
            call_function_name="balanceOf",
            params=[
                self.staking_contract
            ]
        )['0']

    def get_emission_per_second(self):
        return make_call(
            contract_address=self.staking_contract,
            abi_file_name="StakedVeBank",
            call_function_name="assets",
            params=[
                self.staking_contract
            ]
        )["emissionPerSecond"]

    def get_staked_contract_decimals(self):
        return make_call(
            contract_address=self.staking_contract,
            abi_file_name="VIP180",
            call_function_name="decimals",
            params=[]
        )['0']

    def get_staked_token_decimals(self):
        return make_call(
            contract_address=self.staked_token,
            abi_file_name="VIP180",
            call_function_name="decimals",
            params=[]
        )['0']

    def get_staked_token_price(self):
        if self.is_LP:
            _pair = PoolPair(self.staked_token)

            _token0 = Token(_pair.get_token("token0"))
            _token1 = Token(_pair.get_token("token1"))

            _token0_decimals = 10 ** _token0.get_decimals()
            _token1_decimals = 10 ** _token1.get_decimals()

            _token0_price = _token0.get_price()
            _token1_price = _token1.get_price()

            _total_supply = _pair.get_total_lp()
            _reserve0, _reserve1 = _pair.get_reserves()
            _lp_decimals = 10 ** _pair.get_decimals()

            return int(
                (
                    _token0_price / _token0_decimals * _reserve0 / _token0_decimals
                    + _token1_price / _token1_decimals * _reserve1 / _token1_decimals
                )
                / (
                    _total_supply / _lp_decimals
                ) * _lp_decimals
            )
        else:
            _token = Token(self.staked_token)
            _token_price = _token.get_price()
            return _token_price

    def get_rewards_token_decimals(self):
        _rewards_token = Token(self.rewards_token)
        return _rewards_token.get_decimals()

    def get_rewards_token_price(self):
        return Token(self.rewards_token).get_price()

    def get_current_apr(self):
        _emission_per_second = self.get_emission_per_second()
        _rewards_token_decimal = 10 ** Token(self.rewards_token).get_decimals()
        _rewards_token_price = self.get_rewards_token_price()

        _total_staked_tokens = self.get_total_staked()
        _staked_contract_decimals = 10 ** self.get_staked_contract_decimals()
        _staked_token_price = self.get_staked_token_price()

        _p1 = _emission_per_second * AppConstants.SECONDS_IN_YEAR * _rewards_token_price / (_rewards_token_decimal ** 2)
        _p2 = _total_staked_tokens * _staked_token_price / (_staked_contract_decimals ** 2)
        return float(_p1 / _p2)

    def save_apr(self, _apr):
        # _apr = self.get_current_apr()
        StakingAPRModel.insert(
            obj={
                "env": DefaultConfig.ENV,
                "staking_contract": self.staking_contract,
                "apr": _apr
            }
        )
        pass

    def save_total_staked(self):
        _total_token_staked = self.get_total_staked()
        _staked_contract_decimals = 10 ** self.get_staked_contract_decimals()
        _staked_token_price = self.get_staked_token_price()

        StakingTotalModel.insert(
            obj={
                "env": DefaultConfig.ENV,
                "staking_contract": self.staking_contract,
                "total": int(_total_token_staked * _staked_token_price / (_staked_contract_decimals ** 2))
            }
        )
        pass






