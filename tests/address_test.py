from address import check_address_valid, get_address_balance, get_address_ots_keys, get_address_tx_hashes

# write unit test file for the functions in the /src/chainfunctions/address.py file  
# these tests should validate both good and bad values to trigger each instance of the function 
# these will be monitored by codecov in github 

""" 
functions to test the address.py API calls from /src/chainfunctions/address
"""

def test_get_address_balance():
    