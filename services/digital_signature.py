from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


class DigitalSignature:

    def __init__(self):
      
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,  
            key_size=2048  
        )
        self.public_key = self.private_key.public_key()

    def sign(self, message: str) -> bytes:
       
        signature = self.private_key.sign(
            message.encode(), 
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),  
                salt_length=padding.PSS.MAX_LENGTH 
            ),
            hashes.SHA256()  
        )
        return signature

    def verify_signature(self, signature: bytes, message: str) -> bool:
      
        try:
            self.public_key.verify(
                signature,  
                message.encode(),  
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),  
                    salt_length=padding.PSS.MAX_LENGTH  
                ),
                hashes.SHA256()  
            )
            return True  
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False
