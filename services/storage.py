import os
import json
import time
import hashlib
from services.blockchain import Blockchain

class BlockchainWithStorage(Blockchain):
    def __init__(self, storage_file, difficulty=4):
        print(f"Initializing with storage file: {storage_file}")  
        super().__init__(difficulty)  
        self.storage_file = storage_file  
        self.load_from_file()  

    def save_to_file(self):
        try:
            with open(self.storage_file, 'w') as file:
                json.dump(self.chain, file)
            print(f"Blockchain successfully saved to {self.storage_file}")  
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as file:
                    self.chain = json.load(file)
                print(f"Blockchain data loaded from {self.storage_file}")  
            else:
                print(f"File {self.storage_file} not found. Starting with an empty chain.")
        except Exception as e:
            print(f"Error loading from file: {e}")

    def add_block(self, claim_data):
        super().add_block(claim_data) 
        self.save_to_file() 

    def get_chain(self):
        return self.chain  
