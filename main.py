from blockchain import Blockchain
from transaction import Transaction
from wallet import generate_wallet

# Step 1: Create two wallets
wallet_A = generate_wallet()
wallet_B = generate_wallet()

print("Wallet A (public):", wallet_A['public_key'][:10], "...")
print("Wallet B (public):", wallet_B['public_key'][:10], "...")

# Step 2: Create blockchain
mycoin = Blockchain()

# Step 3: Create transaction from A to B
tx1 = Transaction(sender=wallet_A['public_key'], recipient=wallet_B['public_key'], amount=50)
tx1.sign_transaction(wallet_A['private_key'])

# Step 4: Add transaction if valid
if tx1.is_valid():
    mycoin.add_transaction(tx1.__dict__)
else:
    print("Transaction is invalid!")

# Step 5: Mine the transaction
print("\nMining block with pending transaction...")
mycoin.mine_pending_transactions(wallet_A['public_key'])

# Step 6: Show balances (simplified)
def get_balance(address):
    balance = 0
    for block in mycoin.chain:
        for tx in block.transactions:
            if tx['sender'] == address:
                balance -= tx['amount']
            if tx['recipient'] == address:
                balance += tx['amount']
    return balance

print("\nWallet A balance:", get_balance(wallet_A['public_key']))
print("Wallet B balance:", get_balance(wallet_B['public_key']))