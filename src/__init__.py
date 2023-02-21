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

config_file = 'config.ini'
example_config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example')

# is the file there? if not, raise an error and exit
if not os.path.isfile(config_file):
    logging.error(f'Config file {config_file} not found. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} not found. Please copy {example_config_file} to the correct location.')

# is the file empty? if empty exit on failure, log the error and suggest coping the config.ini.example to the correct location
if os.stat(config_file).st_size == 0:
    logging.error(f'Config file {config_file} is empty. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} is empty. Please copy {example_config_file} to the correct location.')

# is the file formatted as a .ini file? if not, raise an error and exit
if not os.path.splitext(config_file)[1] == '.ini':
    logging.error(f'Config file {config_file} is not named as a valid .ini file. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} is not named as a valid .ini file. Please copy {example_config_file} to the correct location.')


# is the content inside the file parsable as a .ini? if not, raise an error and exit
try:
    config = configparser.ConfigParser()
    with open(config_file) as f:
        config.read_file(f)
except configparser.Error:
    logging.error(f'Config file {config_file} is not a valid .ini file. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} is not a valid .ini file. Please copy {example_config_file} to the correct location.')

# check if all sections and keys from example config are present in config file
example_config = configparser.ConfigParser()
with open(example_config_file) as f:
    example_config.read_file(f)

for section in example_config.sections():
    if section not in config:
        logging.warning(f'Section [{section}] is missing from {config_file}. Using defaults.')
    else:
        for key in example_config[section]:
            if key not in config[section]:
                logging.warning(f'Key {key} is missing from section [{section}] in {config_file}. Using default value.')
