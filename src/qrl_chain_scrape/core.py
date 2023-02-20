from qrl_chain_scrape import chainfunctions
from qrl_chain_scrape import config
from qrl_chain_scrape import dbhelper
from qrl_chain_scrape import logginghelper

logging.getLogger(__name__).addHandler(logging.NullHandler()) # set up logging

def main():
    """ Main function. """
    # connect to the database
    connection = dbhelper.connect()
    cursor = dbhelper.get_cursor(connection)

    # get the height of the chain
    chain_height = chainfunctions.get_chain_height()

    # get the height of the last block in the database
    last_block_height = dbhelper.get_last_block_height(cursor)

#    # loop through the blocks and add them to the database
#    for block_height in range(last_block_height, chain_height):
#        # get the block data
#        block_data = chainfunctions.get_block_data(block_height)
#
#        # add the block data to the database
#        dbhelper.add_block_data(cursor, block_data)
#
#        # commit the changes to the database
#        connection.commit()
#
#        # log the block height
#        logging.info('Added block: {}'.format(block_height))

    # close the connection to the database
    connection.close()