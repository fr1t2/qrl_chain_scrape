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
        valid_address = requests.post("http://127.0.0.1:5359/api/IsValidAddress", json=payload)
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
        get_balance = requests.post("http://127.0.0.1:5359/api/GetBalance", json=payload)
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


def get_address_ots_keys(address):
    """
    Get the address OTS keys from the local node for a given address and return it's data in an array.

    Parameters
    ----------
    address : str
        The address to get the OTS keys of.

    Returns
    -------
    list of int
        The address OTS keys in an array.
    """
    try:
        payload = {"address": address}  # using the given address
        get_ots_keys = requests.post("http://127.0.0.1:5359/api/GetOTS", json=payload)
        get_ots_keys.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address ots keys: {}'.format(err))
        raise
    # test that the response is not an error containing a "code" key in the json
    if 'code' in get_ots_keys.json():
        logging.error('Could not get address ots keys: {}'.format(get_ots_keys.json()['error']))
        raise Exception('Could not get address ots keys: {}'.format(get_ots_keys.json()['error']))

    return get_ots_keys.json()['next_unused_ots_index']  # return the address ots keys in an array



def get_address_tx_hashes(address):
    """
    Get the address transaction hashes from the local node for a given address and return it's data in an array.

    Parameters
    ----------
    address : str
        The address to get the transaction hashes of.

    Returns
    -------
    list of str
        The address transaction hashes in an array.
    """

    try:
        payload = {"address": address}  # using the given address
        get_tx_hashes = requests.post("http://127.0.0.1:5359/api/GetTransactions", json=payload)
        get_tx_hashes.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address tx hashes: {}'.format(err))
        raise

    # test that the response is not an error containing a "code" key in the json
    if 'code' in get_tx_hashes.json():
        logging.error('Could not get address tx hashes: {}'.format(get_tx_hashes.json()['error']))
        raise Exception('Could not get address tx hashes: {}'.format(get_tx_hashes.json()['error']))

    address_tx_hashes = []  # create an empty array to store the address tx hashes in
    # loop through the mini_transactions array and get the transaction_hash
    for tx_hash in  get_tx_hashes.json()['mini_transactions']:
        # append to an appropriately named array
        address_tx_hashes.append(tx_hash['transaction_hash'])  

    return address_tx_hashes  # return the address tx hashes in an array




        