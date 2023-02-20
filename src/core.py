import sys

from chainfunctions.block import get_chain_height
from chainfunctions.block import get_block_data
from chainfunctions.address import check_address_valid


if __name__ == "__main__":
    # if the script is passed with a variable "chain" return the height of the chain, 
    # if "chain block" return the block data for the given block, 
    # if "chain tx" return the transaction data for the given transaction
    if len(sys.argv) > 1 and sys.argv[1] == "chain": # if the script passed with variable "chain"
        # if the script passed with variable "chain block" return block data for the block
        if len(sys.argv) > 2 and sys.argv[2] == "block":
            print(f'Get Block: {get_block_data(int(sys.argv[3]))}')
            sys.exit(0)
        # if the script is passed with a variable "address" check if address is valid
        elif len(sys.argv) > 2 and sys.argv[2] == "address":
            # address will need to be passed as well as the variable, so like "address Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728"
            # Check that the user passed in the address to check
            if len(sys.argv) > 3:
                print(f'Check Address: {check_address_valid(sys.argv[3])}')
                sys.exit(0)
            else:
                print("Please pass in an address to check")
                sys.exit(1)

        # if the script is passed with a variable "chain" return the height of the chain
        else:
            print(f'Get Height: {get_chain_height()}')
