from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claimer_name = db.Column(db.String(100), nullable=False)
    claim_details = db.Column(db.String(500), nullable=False)
    digital_signature = db.Column(db.String(500), nullable=False)
    transaction_hash = db.Column(db.String(100))

    def __init__(self, claimer_name, claim_details, digital_signature, transaction_hash=None):
        self.claimer_name = claimer_name
        self.claim_details = claim_details
        self.digital_signature = digital_signature
        self.transaction_hash = transaction_hash
