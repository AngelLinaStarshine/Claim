import hashlib
import json  # Import json module
import time
import rsa  # Import rsa module
import random  # Import random module

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []  # Initialize an empty chain
        self.difficulty = difficulty  # Set the difficulty for proof of work
        # Add the genesis block to the chain (initialize with some data)
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

    def add_block(self, claim_data):
        # Set the previous block's hash
        claim_data['previous_hash'] = self.chain[-1]['hash'] if self.chain else '0'
        
        # Find the proof of work for this block
        claim_data['hash'], claim_data['nonce'] = self.proof_of_work(claim_data)
        
        # Append the new block to the chain
        self.chain.append(claim_data)

    def proof_of_work(self, block):
        # Serialize the block data to a string and encode it into bytes
        block_string = json.dumps(block, sort_keys=True).encode()

        nonce = 0
        while True:
            # Attempt to find a valid hash that satisfies the difficulty requirement
            hash_attempt = hashlib.sha256(block_string + str(nonce).encode()).hexdigest()
            if hash_attempt[:self.difficulty] == '0' * self.difficulty:
                return hash_attempt, nonce
            nonce += 1

    def hash_block(self, block):
        # Serialize the block to a string and hash it using SHA-256
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_chain(self):
        # Return the entire blockchain (list of blocks)
        return self.chain

class DigitalSignature:
    def __init__(self):
        # Generate public and private keys using RSA
        self.private_key, self.public_key = rsa.newkeys(512)

    def generate_signature(self, message):
        message_bytes = message.encode('utf-8')  # Convert message to bytes
        signature = rsa.sign(message_bytes, self.private_key, 'SHA-256')  # Sign the message
        return signature

    def verify_signature(self, signature, message):
        try:
            message_bytes = message.encode('utf-8')  # Convert message to bytes
            rsa.verify(message_bytes, signature, self.public_key)  # Verify the signature
            return True
        except rsa.VerificationError:
            return False

    # Blind the message (apply random factor)
    def blind_message(self, message):
        r = random.randint(1, self.public_key.n - 1)  # Generate the random blinding factor
        blinded_message = (message * pow(r, self.public_key.e, self.public_key.n)) % self.public_key.n
        return blinded_message, r

    # Unblind the message (after the signature is created)
    def unblind_message(self, blinded_message, r):
        r_inverse = pow(r, -1, self.private_key.n)  # Calculate the inverse of r
        original_message = (blinded_message * pow(r_inverse, self.private_key.e, self.private_key.n)) % self.private_key.n
        return original_message

    def sign_blinded_message(self, blinded_message):
        blinded_message_bytes = blinded_message.to_bytes((blinded_message.bit_length() + 7) // 8, byteorder='big')
        blinded_signature = rsa.sign(blinded_message_bytes, self.private_key, 'SHA-256')
        return blinded_signature

    def verify_blinded_signature(self, blinded_message, blinded_signature):
        # Unblind the message first
        r = random.randint(1, self.public_key.n - 1)  # This is typically passed around to unblind
        original_message = self.unblind_message(blinded_message, r)
        original_message_bytes = original_message.to_bytes((original_message.bit_length() + 7) // 8, byteorder='big')

        try:
            rsa.verify(original_message_bytes, blinded_signature, self.public_key)
            return True
        except rsa.VerificationError:
            return False
