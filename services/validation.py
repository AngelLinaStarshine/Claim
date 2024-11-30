import hashlib

class BlockValidator:
    
    @staticmethod
    def validate_block(block, previous_block):
        if previous_block:
            if block['previous_hash'] != previous_block['hash']:
                return False  
        return True
    
    @staticmethod
    def validate_chain(chain, difficulty):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if not BlockValidator.validate_block(current_block, previous_block):
                return False

            if not current_block['hash'].startswith('0' * difficulty):
                return False

        return True
