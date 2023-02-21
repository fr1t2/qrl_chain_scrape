"""write tests for the functions in the ../chainfunctions/block.py module"""


import pytest

# import the functions to be tested
from src import get_chain_height
from src import get_block_data



# get the block height of the chain from the local node and return it
def test_get_chain_height():
    """ Test the get_chain_height() function.
    """
    assert int(get_chain_height()) > 0

def test_get_good_block_data(): 
    """ Test the get_block_data() function.
    """
    block_height = 15
    block_data_recieved = get_block_data(block_height)
    assert block_data_recieved is not None
    assert block_data_recieved != {}
    assert block_data_recieved != []
    assert block_data_recieved != ""
    assert block_data_recieved != 0
    assert block_data_recieved != 0.0
    assert block_data_recieved is not False
    assert block_data_recieved is not True
    assert block_data_recieved != "0"
    assert block_data_recieved != "0.0"
    assert block_data_recieved != "False"
    assert block_data_recieved != "True"
    assert block_data_recieved != "None"
    # assert that it is 15
    assert block_data_recieved['block_height'] == block_height


    #assert get_block_data(block_height) is not None
    #assert get_block_data(block_height) != {}
    #assert get_block_data(block_height) != []
    #assert get_block_data(block_height) != ""
    #assert get_block_data(block_height) != 0
    #assert get_block_data(block_height) != 0.0
    #assert get_block_data(block_height) is not False
    #assert get_block_data(block_height) is not True
    #assert get_block_data(block_height) != "0"
    #assert get_block_data(block_height) != "0.0"
    #assert get_block_data(block_height) != "False"
    #assert get_block_data(block_height) != "True"
    #assert get_block_data(block_height) != "None"

    # assert that it is 15
    assert get_block_data(block_height)['block_number'] == 15

    # assert that it is a dict
    assert isinstance(get_block_data(block_height), dict)



def test_get_bad_block_data(): 
    """ Test the get_block_data() function.
    """
    # get the block data from the local node
    block_height = 0xff

    # assert that we get an exception searching for a block that does not exist using 0xff as the block number
    with pytest.raises(Exception):
        get_block_data(block_height)
