"""
functions to test the address.py API calls from /src/chainfunctions/address
"""
import pytest

from src import check_address_valid, get_address_balance, get_address_ots_keys, get_address_tx_hashes


def test_get_address_balance():
    """
    test the get_address_balance fuction from address.py
    """
    # this should pass as the address is valid
    assert get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        get_address_balance('invalid_address') # invalid address


def test_check_address_valid():
    """
    test the check_address_valid fuction from address.py
    """
    # this should pass as the address is valid
    assert check_address_valid('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        check_address_valid('invalid_address') # invalid address
