""" QRL address related functions"""
import mysql.connector
import requests
import configparser
import logging


# Check if given address is valid
def check_address_valid(address):
    """ Check if an address is valid.

    :param address: the address to check
    :return: True if the address is valid, False otherwise
    """
    # get the address state from the local node
    try:
        payload = {"address": address}  # using the given address
        validAddress = requests.post("http://127.0.0.1:5359/api/IsValidAddress", data=json.dumps(payload))
        validAddress.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address state: {}'.format(err))
        raise

    # get the address state from the response
    address_state = validAddress.json()['state']  # get the address state from the response

    return address_state  # return the address state


# Get the balance of a given address from the local node and return it
def get_address_balance(address):
    """ Get the balance of an address from the local node.

    :param address: the address to get the balance of
    :return: the balance of the address
    """
    # get the address balance from the local node
    try:
        payload = {"address": address}  # using the given address
        getBalance = requests.post("http://127.0.0.1:5359/api/GetTotalBalance", data=json.dumps(payload))
        getBalance.raise_for_status()  # raise an exception if the request fails
    except requests.exceptions.RequestException as err:
        logging.error('Could not get address balance: {}'.format(err))
        raise

    # get the address balance from the response
    address_balance = getBalance.json()['balance']  # get the address balance from the response

    return address_balance  # return the address balance

