"""
QRL Coin Scrape
~~~~~~~~~~~~~~~

QRL Coin Scrape is a blockcghain package meant to scrape the blockchain 
data into a MySQL database for internal application needs.

Gasic Usage:

$ pip3 install qrl-coin-scrape
$ qrl-coin-scrape

See information at https://qrl.co.in/qrl-coin-scrape/docs

 """


# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
from . import _version
__version__ = _version.get_versions()['version']
