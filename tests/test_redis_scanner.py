import argparse
from default_hunter import core
from .test_core import cli_args
from copy import deepcopy
import logging
from unittest import mock


def reset_handlers():
    logger = logging.getLogger("default_hunter")
    logger.handlers = []


redis_args = deepcopy(cli_args)
redis_args["protocols"] = "redis"
redis_args["target"] = "127.0.0.1"


@mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(**redis_args))
def test_redis(mock_args):
    reset_handlers()
    se = core.main()
    assert se.found_q.qsize() == 1
