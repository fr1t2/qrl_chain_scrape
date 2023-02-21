#import configparser
#import os
#import logging
#
## is the file there? if not, raise an error and exit
#if not os.path.isfile('config.ini'):
#    logging.error('Config file not found. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#    raise Exception('Config file not found. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
## is the file empty? if empty exit on failure, log the error and suggest coping the config.ini.example to the correct location
#if os.stat('config.ini').st_size == 0:
#    logging.error('Config file is empty. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#    raise Exception('Config file is empty. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
## is the file formatted as a .ini file? if not, raise an error and exit
#if not os.path.splitext('config.ini')[1] == '.ini':
#    logging.error('Config file is not named as a valid .ini file. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#    raise Exception('Config file is not named in as a valid .ini file. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
#
#
#    # is the content inside the file parsable as a .ini? if not, raise an error and exit
#    try:
#        config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example') # get the path to the config file
#        config = configparser.ConfigParser() # create a new config object
#        config.read(config_file) # read the config file
#    except configparser.Error:
#        logging.error('Config file is not a valid. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#        raise Exception('Config file is not a valid. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
## is the file readable? if not, raise an error and exit
#if not os.access('config.ini', os.R_OK):
#    logging.error('Config file is not readable. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#    raise Exception('Config file is not readable. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
## is the file writable? if not, raise an error and exit
#if not os.access('config.ini', os.W_OK):
#    logging.error('Config file is not writable. Please copy config.ini.example to the correct location /qrl_chain_scrape/src/config.ini.')
#    raise Exception('Config file is not writable. Please copy config.ini.example to the correct location in /qrl_chain_scrape/src/config.ini.')
#
#
## if we get to here, the config file is valid and readable, so we can load it
#config = configparser.ConfigParser() # create a new config object
#config.read(config_file) # read the config file
import configparser
import os
import logging



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
    ex_conf.read_file(example_config_file) # read the config file
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
