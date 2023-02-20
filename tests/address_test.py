"""
functions to test the address.py API calls from /src/chainfunctions/address

large wallet balance: 
Bittrex: Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247

new address (empty) (ots:0)
hexseed: 0105009f913c3b3d69d434a7c975664a9b9ae10e026780c9e367456225163b0895e373f396633d77944a4a1c82c75528301979
pub: Q01050077508d89dcd73be1d8b2458418d2afc9eca0809bd09114087bd3bf948b83a1a9e0d50553

"""
import pytest
import requests

from src import check_address_valid
from src import get_address_balance 
from src import get_address_ots_keys
from src import get_address_tx_hashes


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

def test_get_address_ots_keys_empty_address():
    """test an empty address (no used ots) """
    address = "Q01050077508d89dcd73be1d8b2458418d2afc9eca0809bd09114087bd3bf948b83a1a9e0d50553"
    ots_keys = get_address_ots_keys(address)
    assert ots_keys == (0)

def test_get_address_ots_keys_full_address():
    """test a full address (all ots keys consumed) """
    address = "Q0104000769d2fafe95264a57392049015b556c3df338776d52e278472b64df307c9732fa804da6"
    ots_keys = get_address_ots_keys(address)
    assert ots_keys == (0)

def test_get_address_ots_keys_used_address():
    """test a used address (some ots keys used) """
    address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247"
    ots_keys = get_address_ots_keys(address)

    assert ots_keys > 0  # ots_key_start, we should be greater than that as we have used some keys

def test_get_address_ots_keys_bad_address():
    """test a bad address (not a qrl address) """
    address = "invalid_address"
    with pytest.raises(Exception):
        get_address_ots_keys(address)


def test_get_address_tx_hashes():
    """
    test the get_address_tx_hashes function from address.py
    """
    # this should pass as the address is valid
    assert get_address_tx_hashes('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        get_address_tx_hashes('invalid_address') # invalid address


if __name__ == '__main__':
    pytest.main([__file__])
