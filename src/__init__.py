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

# test the config file opens and fail if not 
try:
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    conf = configparser.ConfigParser() 
    conf.read_file(config_file)  
except:
    logging.error('')
    raise Exception('')

try:
    example_config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example') # get the path to the config file
    ex_conf = configparser.ConfigParser() # create a new config object
    ex_conf.read(example_config_file) # read the config file
except configparser.Error:
    logging.error('Config file is not a valid. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
    raise Exception('Config file is not a valid. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')



# is the file empty? if empty exit on failure, log the error and suggest coping the config.ini.example to the correct location
if os.stat(config_file).st_size == 0:
    logging.error(f'Config file {config_file} is empty. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} is empty. Please copy {example_config_file} to the correct location.')

# is the file formatted as a .ini file? if not, raise an error and exit
if not os.path.splitext(config_file)[1] == '.ini':
    logging.error(f'Config file {config_file} is not named as a valid .ini file. Please copy {example_config_file} to the correct location.')
    raise Exception(f'Config file {config_file} is not named as a valid .ini file. Please copy {example_config_file} to the correct location.')


# is the content inside the file parsable as a .ini? if not, raise an error and exit
#try:
#    config = configparser.ConfigParser()
#    with open(config_file) as f:
#        config.read_file(f)
#except configparser.Error:
#    logging.error(f'Config file {config_file} is not a valid .ini file. Please copy {example_config_file} to the correct location.')
#    raise Exception(f'Config file {config_file} is not a valid .ini file. Please copy {example_config_file} to the correct location.')

# check if all sections and keys from example config are present in config file
for section in ex_conf.sections():
    if section not in conf:
        logging.warning(f'Section [{section}] is missing from {config_file}. Using defaults.')
    else:
        for key in ex_conf[section]:
            if key not in conf[section]:
                logging.warning(f'Key {key} is missing from section [{section}] in {config_file}. Using default value.')
