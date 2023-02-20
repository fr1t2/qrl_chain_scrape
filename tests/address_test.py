from address import check_address_valid, get_address_balance, get_address_ots_keys, get_address_tx_hashes

"""
functions to test the address.py API calls from /src/chainfunctions/address
"""

def test_get_address_balance():
    """
    test the get_address_balance fuction from address.py
    """
    assert get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') # valid address
    assert get_address_balance('invalid_address') # invalid address


"""
with this function:

def test_get_address_balance():
    test the get_address_balance fuction from address.py
    assert get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') == True # valid address
    assert get_address_balance('invalid_address') == False # invalid address
    

Im getting this error:
pylint: warning
C0121 - Comparison 'get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') == True' should be 
'get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') is True' if checking for the singleton value True, 
or 'get_address_balance('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728')' if testing for truthiness (singleton-comparison)
"""



def test_get_address_ots_keys():
    """
    test the get_address_ots_keys fuction from address.py
    """
    assert get_address_ots_keys('Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728') == True
    assert get_address_ots_keys('invalid_address') == False