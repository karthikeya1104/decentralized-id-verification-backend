import json
import os
from web3 import Web3
from django.conf import settings

# Load contract ABI
CONTRACT_ABI_PATH = os.path.join(settings.BASE_DIR, "blockchain", "abi", "DocumentStorageABI.json")
with open(CONTRACT_ABI_PATH) as abi_file:
    CONTRACT_ABI = json.load(abi_file)

# Blockchain connection

CONTRACT_ADDRESS = "0xa6f1e0ca00873bd219487F20E3F0edA24E82590D"  # Replace with your actual contract address
GANACHE_URL = "http://127.0.0.1:7545"  # Update if using other node

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# 🔹 Store a document on-chain
def store_document_on_chain(ipfs_hash, issuer_address, receiver_address, title, issuer_private_key):
    nonce = web3.eth.get_transaction_count(issuer_address)

    txn = contract.functions.storeDocument(
        ipfs_hash,
        receiver_address,
        title
    ).build_transaction({
        'chainId': 1337,
        'gas': 3000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'from': issuer_address,
    })
    
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=issuer_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status != 1:
        raise Exception("Transaction failed")

    # Extract event from receipt using web3's event processor
    events = contract.events.DocumentStored().process_receipt(receipt)
    if not events:
        raise Exception("DocumentStored event not found in transaction logs")

    doc_id = events[0]['args']['id']
    block_tx_hash = events[0]['args']['txHash']  # This is the custom keccak256 hash stored in the contract

    # Return tx_hash (Ethereum tx hash), doc_id, and the contract-generated txHash as hex string
    return tx_hash.hex(), doc_id, block_tx_hash.hex()


# 🔹 Set or unset a document flag (must be issuer or receiver)
def set_document_flag(index, actor_address, actor_private_key, flag_status):
    nonce = web3.eth.get_transaction_count(actor_address)

    txn = contract.functions.setFlag(
        index,
        actor_address,
        flag_status
    ).build_transaction({
        'chainId': 1337,
        'gas': 3000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'from': actor_address,
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=actor_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt.status != 1:
        raise Exception("Flag transaction failed")

    return receipt


def get_document(index):
    return contract.functions.getDocument(index).call()


def get_document_count():
    return contract.functions.getDocumentCount().call()


# 🔹 Verify document by index
def verify_document_by_index(index):
    result = contract.functions.verifyByIndex(index).call()
    # result tuple from contract:
    # (bool exists, string ipfsHash, address issuer, address receiver, string title, uint256 timestamp, bool flagged, bytes32 txHash)
    # Convert txHash bytes32 to hex string for convenience
    exists, ipfsHash, issuer, receiver, title, timestamp, flagged, txHash = result
    txHashHex = web3.to_hex(txHash) if txHash else None
    return (exists, ipfsHash, issuer, receiver, title, timestamp, flagged, txHashHex)


# 🔹 Verify document by tx hash (tx_hash_hex is hex string)
def verify_document_by_tx_hash(tx_hash_hex):
    tx_hash_bytes = web3.to_bytes(hexstr=tx_hash_hex)
    result = contract.functions.verifyByTxHash(tx_hash_bytes).call()
    # result tuple from contract:
    # (bool exists, uint256 index, string ipfsHash, address issuer, address receiver, string title, uint256 timestamp, bool flagged)
    exists, index, ipfsHash, issuer, receiver, title, timestamp, flagged = result
    return (exists, index, ipfsHash, issuer, receiver, title, timestamp, flagged)
