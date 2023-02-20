"""
QRL Coin Scrape
~~~~~~~~~~~~~~~

QRL Coin Scrape is a blockchain package meant to scrape the blockchain
data into a MySQL database for internal application needs.

Basic Usage:

$ pip3 install qrl-coin-scrape
$ qrl-coin-scrape

See information at https://qrl.co.in/qrl-coin-scrape/docs

 """
# __init__.py

import configparser
import os

# Define the path to the configuration file
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# Create a ConfigParser object and read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Make the ConfigParser object available to other modules in the package
from .src.qrl_chain_scrape import chainfunctions
from .src.qrl_chain_scrape import core
from .src.qrl_chain_scrape import db
from .src.qrl_chain_scrape import loggingconf
from .src.qrl_chain_scrape import price
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions




 
#import os
#import configparser
#
#
## Set default logging handler to avoid "No handler found" warnings.
#import logging
#from logging import NullHandler
#
#from . import _version
#__version__ = _version.get_versions()['version']
#
#
#logging.getLogger(__name__).addHandler(NullHandler())
#
#
## Load configuration from file
#config = configparser.ConfigParser()
#config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

## Set up logging
#logging.basicConfig(
#    level=config['logging']['level'],
#    format=config['logging']['format'],
#    datefmt=config['logging']['datefmt']
#)
#
## Set up database connection
#from . import db
#db.connect(
#    host=config['database']['host'],
#    port=config['database']['port'],
#    user=config['database']['user'],
#    password=config['database']['password'],
#    database=config['database']['database']
#)
#
## Set up QRL node connection
#from . import qrl
#qrl.connect(
#    host=config['qrl']['host'],
#    port=config['qrl']['port']
#)
