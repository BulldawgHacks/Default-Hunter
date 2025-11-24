import argparse
from default_hunter import core
from .test_core import cli_args
from copy import deepcopy
import logging
from unittest import mock
import os


logger = logging.getLogger("default_hunter")


def reset_handlers():
    logger = logging.getLogger("default_hunter")
    logger.handlers = []


mongodb_args = deepcopy(cli_args)
mongodb_args["target"] = "mongodb://127.0.0.1"


@mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(**mongodb_args))
def test_mongodb(mock_args):
    reset_handlers()
    se = core.main()
    assert se is not None

    try:
        assert se.found_q.qsize() == 1
    except Exception as e:
        # Raise an assertion error if we're in Travis CI and fail
        if os.environ.get("TRAVIS", None):
            raise e
        # Warn if we're not Travis CI
        else:
            logger.warning("mongodb failed")
