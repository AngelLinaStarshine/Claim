import random
import string
from flask import Blueprint, render_template, request

bp = Blueprint('claims', __name__)

def generate_claim_number():

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@bp.route('/digital_signature', methods=['GET', 'POST'])
def digital_signature():

    claim_number = generate_claim_number()  
    generated_signature = None

    if request.method == 'POST':
        claimer_name = request.form['claimerName']
        incident_details = request.form['incidentDetails']

        generated_signature = f"{claimer_name}:{incident_details}:{claim_number}".encode('utf-8')
        return render_template(
            'index.html',
            claim_number=claim_number,
            generated_signature=generated_signature
        )

    return render_template('digital_signature_form.html')
