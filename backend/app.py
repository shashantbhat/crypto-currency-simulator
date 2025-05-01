from flask import Flask, request, jsonify
from blockchain import Blockchain
from wallet import generate_wallet
from transaction import Transaction

app = Flask(__name__)
bc = Blockchain()
wallets = {}

@app.route("/create-wallet", methods=["GET"])
def create_wallet():
    wallet = generate_wallet()
    wallets[wallet['public_key']] = wallet['private_key']
    return jsonify(wallet)

@app.route("/send", methods=["POST"])
def send_transaction():
    data = request.get_json()
    tx = Transaction(data['sender'], data['recipient'], data['amount'])
    tx.sign_transaction(wallets[data['sender']])
    if tx.is_valid():
        bc.add_transaction(tx.__dict__)
        return jsonify({"message": "Transaction added"}), 201
    return jsonify({"message": "Invalid transaction"}), 400

@app.route("/mine", methods=["POST"])
def mine():
    data = request.get_json()
    bc.mine_pending_transactions(data['miner_address'])
    return jsonify({"message": "Block mined successfully"})

@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = []
    for block in bc.chain:
        chain_data.append({
            "index": block.index,
            "transactions": block.transactions,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "nonce": block.nonce
        })
    return jsonify(chain_data)

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    balance = 0
    for block in bc.chain:
        for tx in block.transactions:
            if tx['sender'] == address:
                balance -= tx['amount']
            if tx['recipient'] == address:
                balance += tx['amount']
    return jsonify({"balance": balance})

if __name__ == "__main__":
    app.run(debug=True)
