""" grab block data from a local node for a given block and return it's data in an array """
import logging
import requests
from chainfunctions import config

# Access the 'walletd' section of the configuration file
API_URL = config.get('walletd', 'url')
API_PORT = config.get('walletd', 'port')
#{API_URL}:{API_PORT}

# get the block height of the chain from the local node and return it
def get_chain_height():
    """ Get the height of the chain from the local node.

    :return: the height of the chain
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



# get the block data from the local node for a given block and return it's data in an array
def get_block_data(block_height):
    """ Get the block data from the local node for a given block and return it's data in an array.

    :param block_height: the height of the block to get
    :return: the block data in an array
    """

    # check if block_height is an integer, even if it is a string of an integer (e.g. "1") and raise exception if not
    
    if not isinstance(block_height, int):
        try:
            block_height = int(block_height)
        except ValueError:
            logging.error('Block height must be an integer')
            raise Exception('Block height must be an integer')
    # get the block data from the local node
    try:
        payload = { "block_number": block_height} # using the given block number
        block_by_number = requests.post(f'{API_URL}:{API_PORT}/api/GetBlockByNumber', json=payload) # 5359 is the default port for the QRL walletd-rest-proxy API
        block_by_number.raise_for_status() # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get block data: {}'.format(err))
        raise Exception('Could not get block data')
    # get the block data from the response
    block_data = block_by_number.json()['block'] # get the block data from the response
    return block_data # return the block data in an array


