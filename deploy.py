
from solcx import compile_standard, install_solc
import json
from web3 import Web3

# read the solidity file
with open("./SimpleStorage.sol", "r") as file:
	simple_storage_file = file.read()
	# print(simple_storage_file)


# installing solc_version  "0.6.0"
install_solc("0.6.0")

# complie our solidity
compiled_sol = compile_standard(
	{
		"language": "Solidity",
		"sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
		"settings": {
			"outputSelection": {
				"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
			}
		},
	},
	solc_version="0.6.0",
)

# print(compiled_sol)

#now gonna dumb the complied code to a json file
with open("compiled_code.json", "w") as file:
	json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
	"bytecode"
]["object"]


#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(bytecode) 

#for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'


#Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode) # contract object before the transaction
#Get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address) #Basically the number of transaction by the curent accnt
#print(nonce)




##1.Build a transaction
##2.Sign a transaction
##3.Send a transaction

#1
transaction = SimpleStorage.constructor().buildTransaction(
	{"chainId":chain_id, "from":my_address, "nonce":nonce}
)
#print(transaction)

#2
signed_transaction = w3.eth.account.sign_transaction(transaction,private_key=private_key)
#print(signed_transaction)

#3
print("Deploying contract..")
transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
# to wait until the transaction happens
transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash) #And, this variable stores the contract address
print("Deplyed!")


#Working with the contract, needed
# contract Address
# contract ABI
simple_storage = w3.eth.contract(address = transaction_receipt.contractAddress, abi=abi) # contract object after the transaction




# To intract with a contract, two ways:
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# for calling a "only return type" function
print(simple_storage.functions.retrive().call()) # Initial value of favorite number

# for a "transact type" function
#1
print("Updating Contract..")
store_transaction = simple_storage.functions.store(15).buildTransaction(
		{"chainId":chain_id, "from":my_address, "nonce":nonce+1}
	) #"nonce" =+1 since after the declaration of the variable we have done one transaction
#2
signed_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
#3
send_store_transaction = w3.eth.sendRawTransaction(signed_store_transaction.rawTransaction)
# wait for the complition of the transaction
transaction_receipt = w3.eth.waitForTransactionReceipt(send_store_transaction)
print("Updated!")
print(simple_storage.functions.retrive().call())