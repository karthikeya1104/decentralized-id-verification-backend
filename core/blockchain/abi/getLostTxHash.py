from web3 import Web3
import json

# Connect to Ganache (or your node)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    print("Error: Web3 provider not connected")
    exit(1)

# Load contract ABI
with open("DocumentStorageABI.json") as f:
    abi = json.load(f)

# Your deployed contract address (check correct casing)
contract_address = "0xF9F5185a8A4F44Ffc1fee30871AAfBCc12256C94"
contract = w3.eth.contract(address=contract_address, abi=abi)

# Receiver address to filter events for (lowercase for comparison)
user_address = "0xadEa32C86041097e663435071f5397d16cF9597b".lower()

# Event signature hash for DocumentStored event
event_signature_hash = w3.keccak(
    text="DocumentStored(uint256,string,address,address,string,uint256,bytes32)"
).hex()

event_signature_hash = "0x" + event_signature_hash

# Get all DocumentStored events by filtering only on event signature
logs = w3.eth.get_logs({
    "fromBlock": 0,
    "toBlock": "latest",
    "address": contract_address,
    "topics": [event_signature_hash]
})

print(f"Found {len(logs)} DocumentStored events in total.\n")

from datetime import datetime

for log in logs:
    # Decode event data using contract ABI
    event = contract.events.DocumentStored().process_log(log)

    # Filter by receiver address manually
    if event.args.receiver.lower() == user_address:
        print(f"Document ID: {event.args.id}")
        print(f"IPFS Hash: {event.args.ipfsHash}")
        print(f"Issuer: {event.args.issuer}")
        print(f"Receiver: {event.args.receiver}")
        print(f"Title: {event.args.title}")
        ts = event.args.timestamp
        print(f"Timestamp: {ts} ({datetime.utcfromtimestamp(ts).isoformat()} UTC)")
        tx_hash_internal = event.args.txHash
        if hasattr(tx_hash_internal, 'hex'):
            tx_hash_internal = tx_hash_internal.hex()
        print(f"Internal keccak txHash: {tx_hash_internal}")
        print(f"Ethereum Transaction Hash: {log['transactionHash'].hex()}")
        print("-" * 50)
