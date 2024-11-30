from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from services.blockchain import Blockchain, DigitalSignature
from services.storage import BlockchainWithStorage
from services.validation import BlockValidator

app = Flask(__name__)
CORS(app)

<<<<<<< HEAD
storage_file = 'blockchain.json'  
=======
storage_file = 'blockchain.json' 
>>>>>>> 50a1e1be7b60a70fe92d62205d01df4e30314987
blockchain = BlockchainWithStorage(storage_file=storage_file, difficulty=4)

digital_signature_service = DigitalSignature()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_claim', methods=['GET', 'POST'])
def submit_claim():
    if request.method == 'GET':
        claim_number = "123456"  
        claim_details = "This is a test claim." 
        return render_template('claim_submission.html', claim_number=claim_number, claim_details=claim_details)

    elif request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                raise ValueError("Missing JSON data")

            claim_number_input = data.get('claimNumber', '').strip()
            claim_signature_input = data.get('claimSignature', '').strip()
            claim_details = data.get('claimDetails', '').strip()

            if not claim_number_input or not claim_signature_input or not claim_details:
                raise ValueError("Missing claim details or signature")

            stored_signature = digital_signature_service.generate_signature(claim_number_input)

            if (claim_number_input == "123456" and 
                claim_signature_input == stored_signature and 
                digital_signature_service.verify_signature(claim_signature_input, claim_number_input)):

                blockchain.add_block({
                    'claim_number': claim_number_input,
                    'claim_details': claim_details,
                    'signature': claim_signature_input
                })

                return redirect(url_for('pending_claims'))

            else:
                return jsonify({"error": "Invalid claim number or signature."}), 400

        except ValueError as e:
            print(f"ValueError: {str(e)}")
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": "Something went wrong, please try again."}), 500

@app.route('/pending_claims', methods=['GET'])
def pending_claims():
    return render_template('pending_claims.html')

if __name__ == '__main__':
    app.run(debug=True)
