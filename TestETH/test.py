import time
from web3 import Web3

# 🔹 Infura API Key (Replace with your own)
INFURA_API_KEY = "c582b514403f4640a5fafe5d0d1ebc2e"
INFURA_URL = f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def w3connect():
    # 🔹 Connect to Sepolia
    if w3.is_connected():
        print("✅ Connected to Sepolia via Infura")
    else:
        print("❌ Connection Failed")
        exit()


# 🔹 Wallet Details
PRIVATE_KEY = "0fcf0b8c984a46d9344f465a9af73d9edeb835e358dfbcf5925591b0a7a43551"  # ⚠️ Never share this
SENDER_ADDRESS = "0xbcaeb05D15c61E5ABf4dB475D8A459449fcD22df"  # Your Sepolia address
RECEIVER_ADDRESS = (
    "0x7daf26D64a62e2e1dB838C84bCAc5bdDb3b5D926"  # Another wallet for selling ETH
)

# # 🔹 Read Single Action from File
# def read_action(file_path):
#     try:
#         with open(file_path, "r") as file:
#             action = int(file.read().strip())  # Read the single number
#             return action
#     except Exception as e:
#         print(f"❌ Error reading action file: {e}")
#         return None


# 🔹 Send ETH Transaction
def send_eth(action):
    if action == 0:
        print("🔹 Action: Keep (No transaction made)")
        return None

    # Define transaction details
    tx = {
        "nonce": w3.eth.get_transaction_count(SENDER_ADDRESS),
        "to": (
            RECEIVER_ADDRESS if action == -1 else SENDER_ADDRESS
        ),  # Sell to recipient, buy = self
        "value": w3.to_wei(0.01, "ether"),  # Amount of ETH to send
        "gas": 21000,
        "gasPrice": w3.to_wei(20, "gwei"),
        "chainId": 11155111,  # Sepolia Chain ID
    }

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Transaction Sent! Tx Hash: {w3.to_hex(tx_hash)}")

    return tx_hash


# # 🔹 Run the Single Action Execution
# file_path = "action.txt"
# action = read_action(file_path)

# if action is not None:
#     if action == 1:
#         print("🟢 Buying ETH...")
#     elif action == -1:
#         print("🔴 Selling ETH...")

#     send_eth(action)
