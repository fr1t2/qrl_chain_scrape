""" grab block data from a local node for a given block and return it's data in an array """
import mysql.connector
import requests
import configparser
import logging
from src import config

# Import the `config` object from the `chainfunctions` package

# Access the 'walletd' section of the configuration file
API_URL = config.get('walletd', 'url')

# get the block height of the chain from the local node and return it
def get_chain_height():
    """ Get the height of the chain from the local node.

    :return: the height of the chain
    """
    # get the block height from the local node
    try:pylint: error
E0602 - Undefined variable 'config' (undefined-variable)
        response = requests.get(f'{API_URL}/GetHeight') # 5359 is the default port for the QRL walletd-rest-proxy API
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error('Could not get chain height: {}'.format(err))
        raise

    return response.json()['height'] # return the height of the chain

# get the block data from the local node for a given block and return it's data in an array
def get_block_data(block_height):
    """ Get the block data from the local node for a given block and return it's data in an array.

    :param block_height: the height of the block to get
    :return: the block data in an array
    """
    # get the block data from the local node
    try:
        payload = { "block_number": block_height} # using the given block number
        getBlockByNumber = requests.post("http://127.0.0.1:5359/api/GetBlockByNumber", data=json.dumps(payload)) # 5359 is the default port for the QRL walletd-rest-proxy API

        getBlockByNumber.raise_for_status() # raise an exception if the request fails

    except requests.exceptions.RequestException as err:
        logging.error('Could not get block data: {}'.format(err))
        raise

    # get the block data from the response
    block_data = getBlockByNumber.json()['block'] # get the block data from the response

    return block_data # return the block data in an array


