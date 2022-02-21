from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))

if w3.isConnected():
    #This line will mess with our autograders, but might be useful when debugging
    #print( "Connected to Ethereum node" )
else:
    print( "Failed to connect to Ethereum node!" )

def get_transaction(tx):
    tx = w3.eth.get_transaction(tx)   #YOUR CODE HERE
    return tx

# Return the gas price used by a particular transaction,
#   tx is the transaction
def get_gas_price(tx):
    gas_price = get_transaction(tx)['gasPrice'] #YOUR CODE HERE
    return gas_price

def get_gas(tx):
    gas = w3.eth.get_transaction_receipt(tx)['gasUsed'] #YOUR CODE HERE
    return gas

def get_transaction_cost(tx):
    tx_cost = get_gas(tx) * get_gas_price(tx) #YOUR CODE HERE
    return tx_cost

def get_block_cost(block_num):
    block_cost = 0  #YOUR CODE HERE
    txs = w3.eth.get_block(block_num)['transactions']
    for tx in txs:
        block_cost += get_transaction_cost(tx)
    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    max_tx = w3.eth.get_block(block_num)['transactions'][0]  #YOUR CODE HERE

    for tx in w3.eth.get_block(block_num)['transactions'][1:]:

        if get_transaction_cost(tx) > get_transaction_cost(max_tx):
            max_tx = tx

    return max_tx
