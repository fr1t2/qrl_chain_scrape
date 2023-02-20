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
from src import parse_qrl_address


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
    # Test a valid address
    address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247"
    keys = get_address_ots_keys(address)
    assert isinstance(keys, int)

    # Test an invalid address
    with pytest.raises(requests.exceptions.RequestException):
        address = "invalid_address"
        keys = get_address_ots_keys(address)

    # Test an address with an error response
    with pytest.raises(Exception):
        address = "error_address"
        keys = get_address_ots_keys(address)

    # Test an address with an empty response
    address = "Q01050077508d89dcd73be1d8b2458418d2afc9eca0809bd09114087bd3bf948b83a1a9e0d50553"
    keys = get_address_ots_keys(address)
    assert keys == 0


def test_get_address_tx_hashes():
    """
    test the get_address_tx_hashes function from address.py
    """
    # this should pass as the address is valid
    assert get_address_tx_hashes('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    # this should fail as the address is invalid
    with pytest.raises(Exception):
        get_address_tx_hashes('invalid_address') # invalid address



def test_parse_qrl_address():
    # Test valid address
    address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247"
    sig_scheme, hash_func, tree_height = parse_qrl_address(address)
    assert sig_scheme == 0
    assert hash_func == 2
    assert tree_height == 4
    
    # Test invalid address - shorter than expected
    with pytest.raises(IndexError):
        address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a22912"
        parse_qrl_address(address)
    
    # Test invalid address - invalid character
    with pytest.raises(ValueError):
        address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a22$1247"
        parse_qrl_address(address)
    
    # Test invalid address - longer than expected
    with pytest.raises(IndexError):
        address = "Q01040062908a55128609363f80102e3c07821eb06d579d0151e575428e9389f4532593a2291247a"
        parse_qrl_address(address)


if __name__ == '__main__':
    pytest.main([__file__])
