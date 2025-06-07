from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load contract ABI
with open("DocumentStorageABI.json") as f:
    abi = json.load(f)

# Your deployed contract address
contract_address = "0xa6f1e0ca00873bd219487F20E3F0edA24E82590D"
contract = w3.eth.contract(address=contract_address, abi=abi)

# Your transaction hash (must include "0x" prefix)
tx_hashes = ["cb16e676a4acaf70af97e13ac5a932233bdcd51d42e50dbf8fb754380f54ab31"]
for tx_hash in tx_hashes:
    tx_hash = "0x" + tx_hash
    # Get the transaction receipt
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    # Decode the DocumentStored event from the receipt
    events = contract.events.DocumentStored().process_receipt(receipt)
    print(events)
    # Print event data
    for event in events:
        print("Document ID:", event.args.id)
        print("IPFS Hash:", event.args.ipfsHash)
        print("Issuer:", event.args.issuer)
        print("Receiver:", event.args.receiver)
        print("Title:", event.args.title)
        print("Timestamp:", event.args.timestamp)
        
        print()