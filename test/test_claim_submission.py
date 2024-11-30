import unittest
from app import app 

class TestClaimSubmission(unittest.TestCase):
    def setUp(self):

        self.client = app.test_client()

    def test_valid_claim_submission(self):
        response = self.client.post('/submit_claim', data={
            'claimNumber': '123456',
            'claimSignature': 'generated_signature',
            'claimDetails': 'Sample claim details'
        })
  
        self.assertEqual(response.status_code, 200)
  
        self.assertIn(b'Claim successfully submitted!', response.data)

    def test_invalid_claim_submission(self):
        response = self.client.post('/submit_claim', data={
            'claimNumber': '123456',
            'claimSignature': 'wrong_signature',
            'claimDetails': 'Sample claim details'
        })
    
        self.assertEqual(response.status_code, 400)

        self.assertIn(b'Invalid claim number or signature.', response.data)

if __name__ == '__main__':
    unittest.main()
