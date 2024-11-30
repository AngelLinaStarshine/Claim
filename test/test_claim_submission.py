import unittest
from app import app  # Import the Flask app from app.py

class TestClaimSubmission(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.client = app.test_client()

    def test_valid_claim_submission(self):
        response = self.client.post('/submit_claim', data={
            'claimNumber': '123456',
            'claimSignature': 'generated_signature',
            'claimDetails': 'Sample claim details'
        })
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the success message is in the response body
        self.assertIn(b'Claim successfully submitted!', response.data)

    def test_invalid_claim_submission(self):
        response = self.client.post('/submit_claim', data={
            'claimNumber': '123456',
            'claimSignature': 'wrong_signature',
            'claimDetails': 'Sample claim details'
        })
        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Check if the error message is in the response body
        self.assertIn(b'Invalid claim number or signature.', response.data)

if __name__ == '__main__':
    unittest.main()
