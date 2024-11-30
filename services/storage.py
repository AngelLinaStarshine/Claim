import os
import json
import time
import hashlib
from services.blockchain import Blockchain

class BlockchainWithStorage(Blockchain):
    def __init__(self, storage_file, difficulty=4):
        print(f"Initializing with storage file: {storage_file}")  # Debugging line to track initialization
        super().__init__(difficulty)  # Initialize the parent Blockchain class
        self.storage_file = storage_file  # Correctly store the storage file path
        self.load_from_file()  # Attempt to load blockchain data from file

    def save_to_file(self):
        try:
            # Make sure to save the blockchain data (self.chain) to the storage file
            with open(self.storage_file, 'w') as file:
                json.dump(self.chain, file)
            print(f"Blockchain successfully saved to {self.storage_file}")  # Debugging line
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self):
        try:
            # If the file exists, load the blockchain data into self.chain
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as file:
                    self.chain = json.load(file)
                print(f"Blockchain data loaded from {self.storage_file}")  # Debugging line
            else:
                # If the file doesn't exist, create an empty chain (starting with genesis block)
                print(f"File {self.storage_file} not found. Starting with an empty chain.")
        except Exception as e:
            print(f"Error loading from file: {e}")

    def add_block(self, claim_data):
        super().add_block(claim_data)  # Call the parent's add_block method
        self.save_to_file()  # Save to file after adding the block

    def get_chain(self):
        return self.chain  # Return the blockchain (list of blocks)
