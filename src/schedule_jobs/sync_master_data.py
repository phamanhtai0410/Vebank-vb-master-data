import time
import sys
import getopt
sys.path.append(".")
from lib.utils import amqp
from src.config import DefaultConfig
from src.extensions import redis_cluster
from src.constants import AppConstants
from src.task import worker


def main(_cfg):
    cfg_rabbit = {
        "hostname": DefaultConfig.RABBIT_HOST, "port": DefaultConfig.RABBIT_PORT,
        "username": DefaultConfig.RABBIT_USER, "password": DefaultConfig.RABBIT_PASSWORD,
        "vhost": DefaultConfig.RABBIT_VHOST, "exchange_type": "topic"
    }
    cfg_rabbit.update(_cfg)
    mq = amqp.AmqpConnection(**cfg_rabbit)
    mq.connect()

    while True:
        mq.publish(
            payload={
                "action": "sync_lending"
            }
        )
        mq.publish(
            payload={
                "action": "sync_staking"
            }
        )
        print("Push to consumer to sync data")
        time.sleep(DefaultConfig.SCHEDULED_INTERVAL)


if __name__ == "__main__":
    _cfg = {}
    _exchange = ""
    _routing_key = ""
    _queue = ""
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "k:e:q:", ["routing_key=", "exchange=", "queue="])
    except getopt.GetoptError:
        print("python3 src/schedule_jobs/sync_master_data.py -e <exchange> -k <routing_key> -q <queue>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("python3 src/schedule_jobs/sync_master_data.py -e <exchange> -k <routing_key> -q <queue>")
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
    main(_cfg)
