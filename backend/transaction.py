import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def sign_transaction(self, private_key_hex):
        if self.sender == "System":
            return
        private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        self.signature = private_key.sign(message).hex()

    def is_valid(self):
        if self.sender == "System":
            return True
        if not self.signature:
            return False
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        public_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
        try:
            return public_key.verify(bytes.fromhex(self.signature), message)
        except:
            return False