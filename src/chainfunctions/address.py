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

    # get the address state from the response
    address_state = valid_address.json()['valid']  # get the address state from the response

    return address_state  # return the address state



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
        print('Address {} balance response {}'.format(address, get_balance.text))
        get_balance.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address balance: {}'.format(err))
        raise

    # get the address balance from the response
    #address_balance = get_balance.json()['balance']  # get the address balance from the response
    address_balance = get_balance.text
    return address_balance  # return the address balance


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

    # get the address ots keys from the response
    address_ots_keys = get_ots_keys.json()['next_unused_ots_index']  # get the address ots keys from the response

    return address_ots_keys  # return the address ots keys in an array



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

    # get the address tx hashes from the response
    address_tx_hashes = get_tx_hashes.json()['mini_transactions']  # get the address tx hashes from the response

    for tx_hash in address_tx_hashes:
        # append to an appropriately named array
        address_tx_hashes.append(tx_hash['transaction_hash'])  # append to an appropriately named array

    return address_tx_hashes  # return the address tx hashes in an array




        