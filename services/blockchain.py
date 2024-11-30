import hashlib
import json
import time
import rsa
import random
import os

class Blockchain:
    def __init__(self, difficulty=4, storage_file='blockchain.json'):
        self.difficulty = difficulty
        self.storage_file = storage_file

        if os.path.exists(self.storage_file):
            self.chain = self.load_chain()
        else:
            self.chain = []
            self.add_block({
                'index': 0,
                'timestamp': time.time(),
                'claim_number': 'genesis_block',
                'claim_details': 'This is the first block.',
                'signature': 'no_signature',
                'previous_hash': '0',
                'hash': self.hash_block({
                    'index': 0,
                    'timestamp': time.time(),
                    'claim_number': 'genesis_block',
                    'claim_details': 'This is the first block.',
                    'signature': 'no_signature',
                    'previous_hash': '0'
                })
            })

    def load_chain(self):
        with open(self.storage_file, 'r') as f:
            return json.load(f)

    def save_chain(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def add_block(self, claim_data):
        claim_data['previous_hash'] = self.chain[-1]['hash'] if self.chain else '0'

        claim_data['hash'], claim_data['nonce'] = self.proof_of_work(claim_data)

        self.chain.append(claim_data)

        self.save_chain()

    def proof_of_work(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()

        nonce = 0
        while True:
            hash_attempt = hashlib.sha256(block_string + str(nonce).encode()).hexdigest()
            if hash_attempt[:self.difficulty] == '0' * self.difficulty:
                return hash_attempt, nonce
            nonce += 1

    def hash_block(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_chain(self):
        return self.chain

class DigitalSignature:
    def __init__(self):
        self.private_key, self.public_key = rsa.newkeys(512)

    def generate_signature(self, message):
        message_bytes = message.encode('utf-8')
        signature = rsa.sign(message_bytes, self.private_key, 'SHA-256')
        return signature

    def verify_signature(self, signature, message):
        try:
            message_bytes = message.encode('utf-8')
            rsa.verify(message_bytes, signature, self.public_key)
            return True
        except rsa.VerificationError:
            return False

    def blind_message(self, message):
        r = random.randint(1, self.public_key.n - 1)
        blinded_message = (message * pow(r, self.public_key.e, self.public_key.n)) % self.public_key.n
        return blinded_message, r

    def unblind_message(self, blinded_message, r):
        r_inverse = pow(r, -1, self.private_key.n)
        original_message = (blinded_message * pow(r_inverse, self.private_key.e, self.private_key.n)) % self.private_key.n
        return original_message

    def sign_blinded_message(self, blinded_message):
        blinded_message_bytes = blinded_message.to_bytes((blinded_message.bit_length() + 7) // 8, byteorder='big')
        blinded_signature = rsa.sign(blinded_message_bytes, self.private_key, 'SHA-256')
        return blinded_signature

    def verify_blinded_signature(self, blinded_message, blinded_signature):
        r = random.randint(1, self.public_key.n - 1)
        original_message = self.unblind_message(blinded_message, r)
        original_message_bytes = original_message.to_bytes((original_message.bit_length() + 7) // 8, byteorder='big')

        try:
            rsa.verify(original_message_bytes, blinded_signature, self.public_key)
            return True
        except rsa.VerificationError:
            return False
