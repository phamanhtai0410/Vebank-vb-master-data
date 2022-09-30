# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class AppConstants(object):
    @staticmethod
    def gen_redis_hash_for_env(_env: str):
        return f"env_{_env}"

    REDIS_HASH_TESTNET = "env_testnet"
    SECONDS_IN_YEAR = 365 * 24 * 3600
    pass
