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
import configparser
import os
import logging
# Import the chainfunctions sub-module
# from src.chainfunctions import *

# Load the configuration file, reporting any failures if found

from core import config