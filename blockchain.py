from web3 import Web3
import json
import os

# Connect to Ganache

GANACHE_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if w3.is_connected():
    print("✅ Web3 connected")
else:
    print("❌ Web3 not connected")




# Load ABI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(BASE_DIR, "SecureDataSharingABI.json")

with open(abi_path, "r") as f:
    contract_abi = json.load(f)

# 🔴 PASTE YOUR DEPLOYED CONTRACT ADDRESS
contract_address = w3.to_checksum_address(
    "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4"
)

# Create contract instance
contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi
)
