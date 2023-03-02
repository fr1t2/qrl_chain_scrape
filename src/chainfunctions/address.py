"""
QRL address related functions

This sub-module contains functions for working with QRL addresses.

Functions:
    check_address_valid(address):
        Check if an address is valid.
    get_address_balance(address):
        Get the balance of an address from the local node.
    get_address_ots_keys(address):
        Get the address ots keys from the local node for a given address and return it's data in an array.
    get_address_tx_hashes(address):
        Get the address tx hashes from the local node for a given address and return it's data in an array.
"""
import logging
import requests

from chainfunctions.config import *

# Access the 'walletd' section of the configuration file
API_URL = config.get('walletd', 'url')
API_PORT = config.get('walletd', 'port')


def check_address_valid(address):
    """
    Check if an address is valid.

    Parameters
    ----------
    address : str
        The address to check.

    Returns
    -------
    bool
        True if the address is valid, False otherwise.
    """
    try:
        payload = {"address": address}  # using the given address
        # 5359 is the default port for the QRL walletd-rest-proxy API
        valid_address = requests.post(f'{API_URL}:{API_PORT}/api/IsValidAddress', json=payload)
        valid_address.raise_for_status()  # raise an exception if the request fails
        logging.info('Address {} is valid'.format(address))  # log that the address is valid
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address state: {}'.format(err))
        raise
    # check for a "code" key in the json as this indicates a failure of some sort. Handle error raising an Exception if so
    if 'code' in valid_address.json():
        logging.error('Could not get address state: {}'.format(valid_address.json()['error']))
        raise Exception('Could not get address state: {}'.format(valid_address.json()['error']))
    return valid_address.json()['valid']

# Get the balance of a given address from the local node and return it
def get_address_balance(address):
    """
    Get the balance of an address from the local node.

    Parameters
    ----------
    address : str
        The address to get the balance of.

    Returns
    -------
    int
        The balance of the address.
    """
    try:
        payload = {"address": address}  # using the given address
        get_balance = requests.post(f'{API_URL}:{API_PORT}/api/GetBalance', json=payload)
        get_balance.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address balance: {}'.format(err))
        raise

    # get the address balance from the response
    #address_balance = get_balance.json()['balance']  # get the address balance from the response

    # if an error occurred the response will be {"code":1,"error":"invalid hex digits in the string"}, else {"balance":"0"}
    # check if the response is an error from the code field
    if 'code' in get_balance.json():
        logging.error('Could not get address balance: {}'.format(get_balance.json()['error']))
        raise Exception('Could not get address balance: {}'.format(get_balance.json()['error']))
    return get_balance.json()['balance']  # return the address balance


def get_address_tx_hashes(address):
    """
    Get the address transaction hashes from the local node for a given address and return it's data in an array.

    Parameters
    ----------
    address : str
        The address to get the transaction hashes of.

    Returns
    -------
    dict
        A dictionary with two keys:
            - 'num_tx': An array with the number of transactions found. If no transactions are found, it will be [0].
            - 'tx_hashes': An array with the transaction hashes.

    Example
    -------
    >>> get_address_tx_hashes('Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247')
    {
        'num_tx': [2],
        'tx_hashes': ['0xabcde...', '0xfghij...']
    }
    """
    try:
        payload = {"address": address}  # using the given address
        get_tx_hashes = requests.post(f'{API_URL}:{API_PORT}/api/GetTransactionsByAddress', json=payload)
        get_tx_hashes.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address tx hashes: {}'.format(err))
        raise

    # test that the response is not an error containing a "code" key in the json
    if 'code' in get_tx_hashes.json():
        logging.error('Could not get address tx hashes: {}'.format(get_tx_hashes.json()['error']))
        raise Exception('Could not get address tx hashes: {}'.format(get_tx_hashes.json()['error']))

    address_tx_hashes = {}  # create an empty array to store the address tx hashes in
    # is the response {}
    if not get_tx_hashes.json(): # is the response {}
        # if it is, return an array with the key "num_tx" set to '0' to indicate no transactions found
        print(f'get_transactions: {get_tx_hashes.json()}')
        # return an array with the key "num_tx" set to '0' to indicate no transactions found
        address_tx_hashes["num_tx"] = [0]
        return address_tx_hashes  # return the address tx hashes in an array
    # if the response is not empty, get the number of transactions found
    address_tx_hashes["num_tx"] = [len(get_tx_hashes.json()['mini_transactions'])] # get the number of transactions found
    # loop through the mini_transactions array and get the transaction_hash
    for tx_hash in  get_tx_hashes.json()['mini_transactions']: 
        # append to an appropriately named array
        address_tx_hashes['tx_hash'] = [tx_hash] # append to an appropriately named array
        # return the address tx hashes in an array with the "num_tx" key added to the array
    return address_tx_hashes  # return the address tx hashes in an array with the "num_tx" key added to the array

def get_address_ots_keys(address):
    """
    Get the next unused OTS key index and total OTS key count of a given QRL address.

    Parameters
    ----------
        address: (str)
            A QRL address string.

    Returns
    -------

        int
            The next unused OTS key index of the given address. 
                If the address has no OTS keys, this function returns 0.

    Raises
    ------
        Exception
            If the request to the QRL walletd_rest_proxy fails or if the response contains an error.

    Example
    -------
    >>> get_address_ots_keys('Q01050077508d89dcd73be1d8b2458418d2afc9eca0809bd09114087bd3bf948b83a1a9e0d50553')
    20

    """
    try:
        payload = {"address": address}  # using the given address
        get_ots_keys = requests.post(f'{API_URL}:{API_PORT}/api/GetOTS', json=payload)
        get_ots_keys.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address ots keys: {}'.format(err))
        raise
    # test that the response is not an error containing a "code" key in the json
    if 'code' in get_ots_keys.json():
        logging.error('Could not get address ots keys: {}'.format(get_ots_keys.json()['error']))
        raise Exception('Could not get address ots keys: {}'.format(get_ots_keys.json()['error']))
    if get_ots_keys.json() == {}:
        # FIXME(fr1t2): Validate if all keys have been used in a given address if ots array is empty or not. #pylint: disable='W0511'
        #   If the QRL walletd_rest_proxy finds a new address or a completely exhausted OTS key it returns an empty array.
        #   Test if this address is used or if it has never been used and somehow return the difference.
        return 0 # return 0 if the address has no OTS keys or is unused...
    return int(get_ots_keys.json()['next_unused_ots_index']) # return the address ots keys and total ots keys as a tuple
