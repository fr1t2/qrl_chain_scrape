"""
functions to test the address.py API calls from /src/chainfunctions/address

new address 
hexseed: 0105009f913c3b3d69d434a7c975664a9b9ae10e026780c9e367456225163b0895e373f396633d77944a4a1c82c75528301979
pub: Q01050077508d89dcd73be1d8b2458418d2afc9eca0809bd09114087bd3bf948b83a1a9e0d50553

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


def test_get_address_ots_keys():
    """
    test the get_address_ots_keys fuction from address.py
    """
    # this should pass as the address is valid
    assert get_address_ots_keys('Q0106004c828d4adf4674d539cafc6f7585ca249c6d23acf5c46bc8bc5821f1cb23cc59a0b6298b') # valid address
    assert get_address_ots_keys('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # new address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        get_address_ots_keys('invalid_address') # invalid address


def test_get_address_tx_hashes():
    """
    test the get_address_tx_hashes fuction from address.py
    """
    # this should pass as the address is valid
    assert get_address_tx_hashes('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        get_address_tx_hashes('invalid_address') # invalid address

