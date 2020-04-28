import json
import logging
import logging.config
import sys
from os.path import abspath, dirname, isfile, join

rel = lambda path: join(dirname(abspath(__file__)), path)  # noqa
sys.path.insert(0, rel("../"))


def get_logger(name):
    fname = rel("./cfg.json")
    assert isfile(
        fname
    ), "You have to configure handlers," " use {} as template".format(fname)
    with open(fname) as f:
        logging.config.dictConfig(json.load(f))
    return logging.getLogger(name)
