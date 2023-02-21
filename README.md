[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3c1e7c527ab94e77a2b0ad58a0af78bd)](https://www.codacy.com/gh/fr1t2/qrl_chain_scrape/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fr1t2/qrl_chain_scrape&amp;utm_campaign=Badge_Grade)

[![Run TODO to Issue](https://github.com/fr1t2/qrl_chain_scrape/actions/workflows/workflow.yml/badge.svg?branch=dev)](https://github.com/fr1t2/qrl_chain_scrape/actions/workflows/workflow.yml)

# Coin-Scrape

This will pull in all of the blockchain data into a mysql database. Is there a better choice, likely however I know MySQL and like to stick with what I am good at.

The process is to pull the block data from the API call found at the documentation site https://docs-beta.theqrl.org/developers/api/walletd-rest-proxy

Basically we will egt the latest block height from the API https://docs-beta.theqrl.org/developers/api/walletd-rest-proxy#getlatestblocknumber

Then we will loop through the block numbers and pull the block data from the API https://docs-beta.theqrl.org/developers/api/walletd-rest-proxy#getblockbynumber

The block data will be stored in a mysql database.

Each nested array in the block data will be stored into a separate table. the insert id of the parent record will be stored in the child record.

the entire program will be written in python 3.7


## Setup

### Install MySQL

ubuntu instructions

```bash
sudo apt-get update
sudo apt-get install mysql-server
```

### Install Python

ubuntu instructions

```bash
sudo apt-get update
sudo apt-get install python3.7
```

### Install Python MySQL Connector

ubuntu instructions

```bash
sudo apt-get update
sudo apt-get install python3-mysqldb
```

### Install Python Requests

ubuntu instructions

```bash
sudo apt-get update
sudo apt-get install python3-requests
```

### Create Database

```sql
CREATE DATABASE qrl;
```

### Create Tables

Creating the table for each area of block data start with the main block data, found in the header of the block data. 
This is the data that is used to identify the block and is used to link the block to the previous block in the chain.

```sql
CREATE TABLE IF NOT EXISTS `block_header` (
  `hash_header` varchar(64) NOT NULL,
  `block_number` bigint(20) NOT NULL,
  `timestamp` bigint(20) NOT NULL,
  `hash_header_prev` varchar(64) NOT NULL,
  `reward_block` bigint(20) NOT NULL,
  `reward_fee` bigint(20) NOT NULL,
  `merkle_root` varchar(64) NOT NULL,
  `mining_nonce` varchar(64) NOT NULL,
  `extra_nonce` varchar(64) NOT NULL,

    PRIMARY KEY (`hash_header`), 
    UNIQUE KEY `block_number` (`block_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the transactions from each block, of which there may be over 100 transactions as seen in the block 0 transaction at https://explorer.theqrl.org/api/block/0 
this table should account for the key values in the transactions array 
break the nested arrays into other tables using the nested key as the table name. ie. coinbase, transfer, token_tx, etc. 

```sql
CREATE TABLE IF NOT EXISTS `block_transactions` (
  `hash_header` varchar(64) NOT NULL,
  `master_addr` varchar(64) NOT NULL,
  `nonce` bigint(20) NOT NULL,
  `transaction_hash` varchar(64) NOT NULL,
  `fee` bigint(20) ,
  `public_key` varchar(128),
  `signature` varchar(128) ,
  `signer_addr` varchar(64) ,

    PRIMARY KEY (`tx_hash`), # this is not right
    UNIQUE KEY `transaction_hash` (`transaction_hash`),
    KEY `hash_header` (`hash_header`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the coinbase transaction, which is the first transaction in the block and is used to reward the miner for mining the block. 
This table should account for the key values in the coinbase array.

```sql
CREATE TABLE IF NOT EXISTS `block_coinbase` (
  `transaction_hash` varchar(64) NOT NULL,
  `addr_to` varchar(64) NOT NULL,
  `amount` bigint(20) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`),
    KEY `addr_to` (`addr_to`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the transfer transaction, which is used to transfer QRL from one address to another. 

This table should account for the key values in the transfer array and link multiple addresses to the same transaction hash if needed.

```sql
CREATE TABLE IF NOT EXISTS `block_transfer` (
  `transaction_hash` varchar(64) NOT NULL,
  `addr_to` varchar(64) NOT NULL,
  `amount` bigint(20) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`),
    KEY `addr_to` (`addr_to`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the token tx, which is used to create a token from a master address. There are a bit more values in this function.

This table should account for the key values in the token_tx array and link multiple addresses to the same transaction hash if needed.

```sql
CREATE TABLE IF NOT EXISTS `block_token_tx` (
  `transaction_hash` varchar(64) NOT NULL,
  `addr_to` varchar(64) NOT NULL,
  `amount` bigint(20) NOT NULL,
  `symbol` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `owner` varchar(64) NOT NULL,
  `decimals` int(11) NOT NULL,
  `initial_balances` bigint(20) NOT NULL,
  `initial_balances_addr` varchar(64) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`),
    KEY `addr_to` (`addr_to`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the token transaction, which is used to transfer tokens from one address to another. 

This table should account for the key values in the token_tx array and link multiple addresses to the same transaction hash if needed.

```sql
CREATE TABLE IF NOT EXISTS `block_token_tx` (
  `transaction_hash` varchar(64) NOT NULL,
  `addr_to` varchar(64) NOT NULL,
  `amount` bigint(20) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`),
    KEY `addr_to` (`addr_to`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the slave transaction, which is used to create a slave address. 

This table should account for the key values in the slave array.

```sql
CREATE TABLE IF NOT EXISTS `block_slave` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the lattice transaction, which is used to create a lattice address. 

This table should account for the key values in the lattice array.

```sql
CREATE TABLE IF NOT EXISTS `block_lattice` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```



The next table is for the message transaction which is used to send a message to another address. 

This table should account for the key values in the message array.

```sql
CREATE TABLE IF NOT EXISTS `block_message` (
  `transaction_hash` varchar(64) NOT NULL,
  `message_hash` varchar(64) NOT NULL,
  `message` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the vote transaction which is used to vote for a specific miner. 

This table should account for the key values in the vote array.

```sql
CREATE TABLE IF NOT EXISTS `block_vote` (
  `transaction_hash` varchar(64) NOT NULL,
  `vote` varchar(64) NOT NULL,
  `voter` varchar(64) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### MultiSigCreate

The next table is for the multi sig transaction which is used to create a multi sig address. 

This table should account for the key values in the multi_sig array.

from this link https://github.com/theQRL/QRL/blob/master/src/qrl/protos/qrl.proto construct the remaining tables and fields.

```sql
CREATE TABLE IF NOT EXISTS `block_multi_sig` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

The next table is for the multi sig spend transaction which is used to spend from a multi sig address. 

This table should account for the key values in the multi_sig_spend array.

#### MultiSigSpend

```sql
CREATE TABLE IF NOT EXISTS `block_multi_sig_spend` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```


#### MultiSigVote

```sql
CREATE TABLE IF NOT EXISTS `block_multi_sig_vote` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```



#### ProposalCreate
        
```sql
CREATE TABLE IF NOT EXISTS `block_proposal_create` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### ProposalVote

```sql
CREATE TABLE IF NOT EXISTS `block_proposal_vote` (
  `transaction_hash` varchar(64) NOT NULL,
  `access_type` varchar(64) NOT NULL,
  `fee` bigint(20) NOT NULL,
  `xmss_pk` varchar(128) NOT NULL,

    PRIMARY KEY (`transaction_hash`),
    UNIQUE KEY `transaction_hash` (`transaction_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

## Script flow

Using the tables from above, grab a block starting with 0 using the https://docs-beta.theqrl.org/developers/api/walletd-rest-proxy#getblockbynumber function 

Loop through the transactions in the block and insert the data into the tables.

```python
import json
import requests

payload = { "block_number": "114714"}
getBlockByNumber = requests.post("http://127.0.0.1:5359/api/GetBlockByNumber", data=json.dumps(payload))

block = getBlockByNumber.json()
```


then inserting the data into the database

```python
import mysql.connector

cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost', database='qrl')

cursor = cnx.cursor()

add_block = ("INSERT INTO block "
               "(block_number, block_hash, prev_block_hash, timestamp, nonce, reward, fee_reward, blockheader_hash, miner_address) "
               "VALUES (%(block_number)s, %(block_hash)s, %(prev_block_hash)s, %(timestamp)s, %(nonce)s, %(reward)s, %(fee_reward)s, %(blockheader_hash)s, %(miner_address)s)")

data_block = {
  'block_number': block['block_number'],
  'block_hash': block['block_hash'],
  'prev_block_hash': block['prev_block_hash'],
  'timestamp': block['timestamp'],
  'nonce': block['nonce'],
  'reward': block['reward'],
  'fee_reward': block['fee_reward'],
  'blockheader_hash': block['blockheader_hash'],
  'miner_address': block['miner_address']
}

cursor.execute(add_block, data_block)

block_number = block['block_number']

for transaction in block['transactions']:
    if transaction['transaction_type'] == "transfer":
        add_transfer = ("INSERT INTO block_transfer "
                       "(transaction_hash, fee, xmss_pk, master_addr, slave_addr, amount, ots_key) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(master_addr)s, %(slave_addr)s, %(amount)s, %(ots_key)s)")

        data_transfer = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'master_addr': transaction['master_addr'],
          'slave_addr': transaction['slave_addr'],
          'amount': transaction['amount'],
          'ots_key': transaction['ots_key']
        }

        cursor.execute(add_transfer, data_transfer)
    elif transaction['transaction_type'] == "message":
        add_message = ("INSERT INTO block_message "
                       "(transaction_hash, fee, xmss_pk, message_hash, message) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(message_hash)s, %(message)s)")

        data_message = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'message_hash': transaction['message_hash'],
          'message': transaction['message']
        }

        cursor.execute(add_message, data_message)
    elif transaction['transaction_type'] == "token":
        add_token = ("INSERT INTO block_token "
                       "(transaction_hash, fee, xmss_pk, symbol, name, owner, decimals, initial_balances, ots_key) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(symbol)s, %(name)s, %(owner)s, %(decimals)s, %(initial_balances)s, %(ots_key)s)")

        data_token = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'symbol': transaction['symbol'],
          'name': transaction['name'],
          'owner': transaction['owner'],
          'decimals': transaction['decimals'],
          'initial_balances': transaction['initial_balances'],
          'ots_key': transaction['ots_key']
        }

        cursor.execute(add_token, data_token)
    elif transaction['transaction_type'] == "latticePK":
        add_latticePK = ("INSERT INTO block_latticePK "
                       "(transaction_hash, fee, xmss_pk, slave_pks, ots_key) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(slave_pks)s, %(ots_key)s)")

        data_latticePK = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'slave_pks': transaction['slave_pks'],
          'ots_key': transaction['ots_key']
        }

        cursor.execute(add_latticePK, data_latticePK)
    elif transaction['transaction_type'] == "latticeSignature":
        add_latticeSignature = ("INSERT INTO block_latticeSignature "
                       "(transaction_hash, fee, xmss_pk, message_hash, message, slave_pks, ots_key) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(message_hash)s, %(message)s, %(slave_pks)s, %(ots_key)s)")

        data_latticeSignature = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'message_hash': transaction['message_hash'],
          'message': transaction['message'],
          'slave_pks': transaction['slave_pks'],
          'ots_key': transaction['ots_key']
        }

        cursor.execute(add_latticeSignature, data_latticeSignature)
    elif transaction['transaction_type'] == "slave":
        add_slave = ("INSERT INTO block_slave "
                       "(transaction_hash, fee, xmss_pk, slave_pks, ots_key) "
                       "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(slave_pks)s, %(ots_key)s)")

        data_slave = {
          'transaction_hash': transaction['transaction_hash'],
          'fee': transaction['fee'],
          'xmss_pk': transaction['xmss_pk'],
          'slave_pks': transaction['slave_pks'],
          'ots_key': transaction['ots_key']
        }

        cursor.execute(add_slave, data_slave)
    elif transaction['transaction_type'] == "transfer_token":
        add_transfer_token = ("INSERT INTO block_transfer_token "
                       "(transaction_hash, fee, xmss_pk, token_txhash, owner, slave, amount, ots_key) "
                          "VALUES (%(transaction_hash)s, %(fee)s, %(xmss_pk)s, %(token_txhash)s, %(owner)s, %(slave)s, %(amount)s, %(ots_key)s)")
    
        data_transfer_token = {
            'transaction_hash': transaction['transaction_hash'],
            'fee': transaction['fee'],
            'xmss_pk': transaction['xmss_pk'],
            'token_txhash': transaction['token_txhash'],
            'owner': transaction['owner'],
            'slave': transaction['slave'],
            'amount': transaction['amount'],
            'ots_key': transaction['ots_key']
            }

        cursor.execute(add_transfer_token, data_transfer_token)

def get_blockchain(cursor):
    cursor.execute("SELECT * FROM block")
    blocks = cursor.fetchall()
    return blocks

def get_block(cursor, block_number):
    cursor.execute("SELECT * FROM block WHERE block_number = %s", (block_number,))
    block = cursor.fetchone()
    return block

def get_block_transactions(cursor, block_number):
    cursor.execute("SELECT * FROM block WHERE block_number = %s", (block_number,))
    block = cursor.fetchone()
    transactions = []
    if block['transaction_1'] != None:
        transactions.append(get_transaction(cursor, block['transaction_1']))
    if block['transaction_2'] != None:
        transactions.append(get_transaction(cursor, block['transaction_2']))
    if block['transaction_3'] != None:
        transactions.append(get_transaction(cursor, block['transaction_3']))
    if block['transaction_4'] != None:
        transactions.append(get_transaction(cursor, block['transaction_4']))
    if block['transaction_5'] != None:
        transactions.append(get_transaction(cursor, block['transaction_5']))
    if block['transaction_6'] != None:
        transactions.append(get_transaction(cursor, block['transaction_6']))
    if block['transaction_7'] != None:
        transactions.append(get_transaction(cursor, block['transaction_7']))
    if block['transaction_8'] != None:
        transactions.append(get_transaction(cursor, block['transaction_8']))
    if block['transaction_9'] != None:
        transactions.append(get_transaction(cursor, block['transaction_9']))
    if block['transaction_10'] != None:
        transactions.append(get_transaction(cursor, block['transaction_10']))
    return transactions

def get_transaction(cursor, transaction_hash):
    cursor.execute("SELECT * FROM block_coinbase WHERE transaction_hash = %s", (transaction_hash,))
    transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_message WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_transfer WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_multi_sig WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_token WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_latticePK WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_latticeSignature WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_slave WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    if transaction == None:
        cursor.execute("SELECT * FROM block_transfer_token WHERE transaction_hash = %s", (transaction_hash,))
        transaction = cursor.fetchone()
    return transaction

def get_block_number(cursor, block_hash):
    cursor.execute("SELECT block_number FROM block WHERE block_hash = %s", (block_hash,))
    block_number = cursor.fetchone()
    return block_number

def get_block_hash(cursor, block_number):
    cursor.execute("SELECT block_hash FROM block WHERE block_number = %s", (block_number,))
    block_hash = cursor.fetchone()
    return block_hash

def get_block_timestamp(cursor, block_number):
    cursor.execute("SELECT timestamp FROM block WHERE block_number = %s", (block_number,))
    timestamp = cursor.fetchone()
    return timestamp

def get_block_difficulty(cursor, block_number):
    cursor.execute("SELECT difficulty FROM block WHERE block_number = %s", (block_number,))
    difficulty = cursor.fetchone()
    return difficulty

def get_block_nonce(cursor, block_number):
    cursor.execute("SELECT nonce FROM block WHERE block_number = %s", (block_number,))
    nonce = cursor.fetchone()
    return nonce

def get_block_reward(cursor, block_number):
    cursor.execute("SELECT reward FROM block WHERE block_number = %s", (block_number,))
    reward = cursor.fetchone()
    return reward

def get_block_size(cursor, block_number):
    cursor.execute("SELECT size FROM block WHERE block_number = %s", (block_number,))
    size = cursor.fetchone()
    return size

def get_block_previous_hash(cursor, block_number):
    cursor.execute("SELECT previous_hash FROM block WHERE block_number = %s", (block_number,))
    previous_hash = cursor.fetchone()
    return previous_hash

def get_block_signature(cursor, block_number):
    cursor.execute("SELECT signature FROM block WHERE block_number = %s", (block_number,))
    signature = cursor.fetchone()
    return signature

def get_block_public_key(cursor, block_number):
    cursor.execute("SELECT public_key FROM block WHERE block_number = %s", (block_number,))
    public_key = cursor.fetchone()
    return public_key


def get_block_transaction_count(cursor, block_number):
    cursor.execute("SELECT transaction_count FROM block WHERE block_number = %s", (block_number,))
    transaction_count = cursor.fetchone()
    return transaction_count


```

with the data in the database, another function will run to update every new block that gets added.

New blocks happen on average every 60 seconds

```python
def update_blockchain():
    cursor = db.cursor()
    cursor.execute("SELECT block_number FROM block ORDER BY block_number DESC LIMIT 1")
    last_block_number = cursor.fetchone()
    if last_block_number == None:
        last_block_number = 0
    else:
        last_block_number = last_block_number['block_number']
    current_block_number = get_block_number()
    if current_block_number > last_block_number:
        for block_number in range(last_block_number + 1, current_block_number + 1):
            block = get_block(block_number)
            if block != None:
                add_block(cursor, block)
                print("Added block " + str(block_number))
            else:
                print("Block " + str(block_number) + " does not exist")
        db.commit()
    cursor.close()
```


## Conclusion

This is a simple script that can be used to create a database of the blockchain. 

