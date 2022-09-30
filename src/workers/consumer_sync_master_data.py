import json
import sys
import getopt

sys.path.append(".")
from lib.utils import amqp
from pydash import get
from lib.logger import LoggerTask
from src.task import worker
from src.helpers.vechain import *
from src.config import DefaultConfig
from src.extensions import redis_cluster
from src.constants import AppConstants
from src.helpers.staking import Staking
from pymodm import connect
from lib.enums.database import DBName


def lending_handler():
    # Collect data from blockchain

    # Sync to redis cluster

    # Save to DB
    pass


def staking_handler():
    # Get all staking contracts
    _VB_address = redis_cluster.hget(
            AppConstants.gen_redis_hash_for_env(DefaultConfig.ENV),
            "VB"
        )
    _LP_address = redis_cluster.hget(
            AppConstants.gen_redis_hash_for_env(DefaultConfig.ENV),
            "LP_VB_VET"
        )

    _staking_VB = Staking(
        redis_cluster.hget(
            AppConstants.gen_redis_hash_for_env(DefaultConfig.ENV),
            "STAKING_CONTRACT_VB"
        ),
        _VB_address,
        _VB_address
    )
    _staking_LP_VB_VET = Staking(
        redis_cluster.hget(
            AppConstants.gen_redis_hash_for_env(DefaultConfig.ENV),
            "STAKING_CONTRACT_LP_VB_VET"
        ),
        _LP_address,
        _VB_address,
        True
    )
    # Collect data from blockchain
    _apr_VB = _staking_VB.get_current_apr()
    _apr_LP = _staking_LP_VB_VET.get_current_apr()
    print("*** APR : ", _apr_LP, _apr_VB)
    # Save to DB
    _staking_VB.save_apr(_apr_VB)
    _staking_LP_VB_VET.save_apr(_apr_LP)
    pass


def on_message_sync_master_data(channel, method, properties, body):
    try:
        msg = body.decode("utf8")
        msg = json.loads(msg)
        _data_msg = msg
        # Log received message
        LoggerTask.debug(_data_msg)
        _args = get(_data_msg, "returnValues")
        _action = get(_data_msg, "action")

        if _action == "sync_lending":
            lending_handler()
        elif _action == 'sync_staking':
            staking_handler()
        else:
            print("Action not found")
            sys.exit(2)

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(e)
        channel.basic_nack(delivery_tag=method.delivery_tag)


def handle_msg(_cfg):
    cfg_rabbit = {
        "hostname": DefaultConfig.RABBIT_HOST, "port": DefaultConfig.RABBIT_PORT,
        "username": DefaultConfig.RABBIT_USER, "password": DefaultConfig.RABBIT_PASSWORD,
        "vhost": DefaultConfig.RABBIT_VHOST, "exchange_type": "topic"
    }
    cfg_rabbit.update(_cfg)
    event_name = cfg_rabbit["queue"].split("-")[-1]
    print("cfg_rabbit: ", cfg_rabbit)
    mq = amqp.AmqpConnection(**cfg_rabbit)
    mq.connect()
    mq.setup_queues(durable=True)

    connect(DefaultConfig.DB_APP, connect=False, alias=DBName.ANALYTIC)

    if event_name == "sync_master_data":
        mq.consume(on_message_sync_master_data)
    else:
        print("Event not found")
        sys.exit(2)


if __name__ == "__main__":
    _cfg = {}
    _exchange = ""
    _routing_key = ""
    _queue = ""
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "k:e:q:", ["routing_key=", "exchange=", "queue="])
    except getopt.GetoptError:
        print("python3 workers/consumer_sync_master_data.py -e <exchange> -k <routing_key> -q <queue>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("python3 workers/consumer_sync_master_data.py -e <exchange> -k <routing_key> -q <queue>")
            sys.exit()
        elif opt in ("-e", "--exchange"):
            _exchange = arg
        elif opt in ("-k", "--routing_key"):
            _routing_key = arg
            print("_routing_key: ", _routing_key)
        elif opt in ("-q", "--queue"):
            _queue = arg

    _cfg["exchange"] = _exchange
    _cfg["routing_key"] = _routing_key
    _cfg["queue"] = _queue
    handle_msg(_cfg)
