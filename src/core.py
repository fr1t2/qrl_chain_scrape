import sys

from .chainfunctions import get_chain_height
from .chainfunctions.block import get_block_data
from .chainfunctions.address import check_address_valid
from chainfunctions.address import get_address_balance
from chainfunctions.address import get_address_ots_keys
from chainfunctions.address import get_address_tx_hashes

#if __name__ == "__main__":
# if the script is passed with a variable "chain" return the height of the chain, 
# if "chain block" return the block data for the given block, 
# if "chain tx" return the transaction data for the given transaction
if len(sys.argv) > 1 and sys.argv[1] == "chain": # if the script passed with variable "chain"
    # if the script passed with variable "chain block" return block data for the block
    if len(sys.argv) > 2 and sys.argv[2] == "block":
        # block will need to be passed as well as the variable, so like "block 1" or "block 100"
        # for each block up to number given, fetch the data and return in large array of block data
        if len(sys.argv) > 3:
            if sys.argv[3] == "single":
                if sys.argv[4].isdigit():
                    print(f'Get Block: {get_block_data(int(sys.argv[4]))}')
                    sys.exit(0)
                else:
                    print("Block number must be an integer")
                    sys.exit(0)
            elif sys.argv[3] == "range":
                if sys.argv[4].isdigit() and sys.argv[5].isdigit():
                    block_data = {}
                    for block in range(int(sys.argv[4]), int(sys.argv[5])):
                        block_data[block] = get_block_data(block)
                    print(f'Get Block: {block_data}')
                    sys.exit(0)
                else:
                    print("Block numbers must be an integer and provided in a range {1 100}")
                    sys.exit(0)
            else:
                print("Block must be single or range")
                sys.exit(0)
        else:
            print("Block number must be provided")
            sys.exit(0)
    # if the script passed with variable "chain tx" return transaction data for the transaction
        sys.exit(0)
    # if the script is passed with a variable "address" check if address is valid
    elif len(sys.argv) > 2 and sys.argv[2] == "address":
        # address will need to be passed as well as the variable, so like "address Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728"
        # check if "address balance Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728" passed and give the balance
        if len(sys.argv) > 3 and sys.argv[3] == "balance":
            print(f'Check Address Balance: {get_address_balance(sys.argv[4])}')
            sys.exit(0)
        # check ots keys
        elif len(sys.argv) > 3 and sys.argv[3] == "ots":
            print(f'Check Address OTS Keys: {get_address_ots_keys(sys.argv[4])}')
            sys.exit(0)
        elif len(sys.argv) > 3 and sys.argv[3] == "tx":
            print(f'Check Address TX Hashes: {get_address_tx_hashes(sys.argv[4])}')
            sys.exit(0)
        # check if "address Q010500dacbf29a83ef6832bcf16f0592adb15313836228a873a7b8eed1c354c4414a206ad38728" passed and give validity
        elif len(sys.argv) > 3:
            print(f'Check Address: {check_address_valid(sys.argv[3])}')
            sys.exit(0)
        # if no address passed, exit with error
        else:
            print("Please pass in an address to check")
            sys.exit(1)

    # if the script is passed with a variable "chain" return the height of the chain
    else:
        print(f'Get Height: {get_chain_height()}')
