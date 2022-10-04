import sys
sys.path.append(".")
from src.extensions import redis_cluster
from pydash import get


def run():
    _env = "dev"
    _key_name = f"vb.env_{_env}"
    _configurations = [
        {
            "name": "VB",
            "value": "0xe88c871CEA576DdD59FA91a744Eb6C6d5b93AB40"
        },
        {
            "name": "LP_VB_VET",
            "value": "0x31e3fd68f0223bbb64a8a495d6a58daf39bbc4ff"
        },
        {
            "name": "STAKING_CONTRACT_VB",
            "value": "0x24cd98E51A07fac229733DB6DF4BBbe8AA69cd9A"
        },
        {
            "name": "STAKING_CONTRACT_LP_VB_VET",
            "value": "0x2E29E7907F5Efa453052eD3a0c77B964CEA13C6e"
        },
        {
            "name": "SEER_BTCUSD",
            "value": "0x18A2fEAae2fA06B3452fd094Ba802C93FF0dA972"
        },
        {
            "name": "SEER_ETHUSD",
            "value": "0xed8e829cfEB0Cdd315C26c7df10e81B12a3abA95"
        },
        {
            "name": "SEER_VTHOUSD",
            "value": "0x5E7A52743575FE6F8cD8937C0415640338eBdd29"
        },
        {
            "name": "SEER_VETUSD",
            "value": "0x3212feD5581DEFbb2d7Ea21d7F22f657cD3da97E"
        },
        {
            "name": "SEER_VBUSD",
            "value": "0xDf925feC9932A1De0d2b4404cCfac09166624F94"
        },
        {
            "name": "SEER_VEUSDUSD",
            "value": "0xA2B0d7b38dc13a58A7B4c0E8E2400d650dad46EC"
        }
    ]
    for _index in range(len(_configurations)):
        redis_cluster.hset(
            name=_key_name,
            key=get(_configurations[_index], "name"),
            value=get(_configurations[_index], "value")
        )
    print("Script config done !")


if __name__ == "__main__":
    run()
