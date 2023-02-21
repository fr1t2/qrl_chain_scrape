"""write tests for the functions in the ../chainfunctions/block.py module"""

# using pytest 
# https://docs.pytest.org/en/latest/
# https://docs.pytest.org/en/latest/getting-started.html#getstarted

# import the functions to be tested
from src.chainfunctions.block import get_chain_height, get_block_data

# import the requests module
import requests

# import the logging module
import logging

# import the config module
from src import config

# import the pytest module
import pytest

#no

# Access the 'walletd' section of the configuration file
API_URL = config.get('walletd', 'url')
API_PORT = config.get('walletd', 'port')
#{API_URL}:{API_PORT}

# get the block height of the chain from the local node and return it
def test_get_chain_height():
    """ Test the get_chain_height() function.
    """
    # get the block height from the local node
    try:
        response = requests.get(f'{API_URL}:{API_PORT}/api/GetHeight') # 5359 is the default port for the QRL walletd-rest-proxy API
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error('Could not get chain height: {}'.format(err))
        raise Exception('Could not get chain height')

        # test for empty array {} and raise exception if it is
        if response.json() == {}:
            logging.error('No data returned from the node')
            raise Exception('No data returned from the node')

    # get the block height from the response
    return response.json()['height'] # return the height of the chain

block_height = 15

# get the block data from the local node for a given block and return it's data in an array
def test_get_good_block_data(block_height):
    """ Test the get_block_data() function.
    """
    # get the block data from the local node
    try:
        payload = { "block_number": block_height} # using the given block number
        block_by_number = requests.post(f'{API_URL}:{API_PORT}api/GetBlockByNumber', json=payload) # 5359 is the default port for the QRL walletd-rest-proxy API
        block_by_number.raise_for_status() # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get block data: {}'.format(err))
        raise Exception('Could not get block data')
    # get the block data from the response
    block_data = block_by_number.json()['block'] # get the block data from the response
    return block_data # return the block data in an array
