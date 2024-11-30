function verifySignature() {
    const enteredSignature = document.getElementById('claimSignature').value.trim();
    const storedGeneratedSignature = localStorage.getItem('generatedSignature'); 
    const storedClaimNumber = localStorage.getItem('claimNumber'); 
    const storedClaimDetails = localStorage.getItem('claimDetails'); 

    if (enteredSignature === storedGeneratedSignature) {
    
        document.getElementById('claimNumberDisplay').innerText = storedClaimNumber;
        document.getElementById('claimDetailsDisplay').innerText = storedClaimDetails;
        document.getElementById('claimDetailsSection').style.display = 'block';  

        Swal.fire({
            title: 'Success!',
            text: 'Digital signature verified successfully.',
            icon: 'success',
            confirmButtonText: 'Proceed to Submit Claim'
        });

        addSubmitEventListener();
    } else {
        Swal.fire({
            title: 'Error!',
            text: 'The digital signature does not match. Please check and try again.',
            icon: 'error',
            confirmButtonText: 'Retry'
        });
    }
}

function submitClaim(event) {
    event.preventDefault();  

    const claimNumberElement = document.getElementById('claimNumber');
    const claimSignatureElement = document.getElementById('claimSignature');
    const claimDetailsElement = document.getElementById('claimDetails');

    console.log(claimNumberElement, claimSignatureElement, claimDetailsElement);  

    if (!claimNumberElement || !claimSignatureElement || !claimDetailsElement) {
        alert('Some form elements are missing.');
        return;
    }

    // Get the claim data
    const claimData = {
        claimNumber: claimNumberElement.value,
        claimSignature: claimSignatureElement.value,
        claimDetails: claimDetailsElement.value
    };

  
    if (!claimData.claimNumber || !claimData.claimSignature || !claimData.claimDetails) {
        alert('Please fill in all fields');
        return;
    }

    fetch('/submit_claim', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(claimData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Claim submitted successfully:', data);
        window.location.href = '/pending_claims';  
    })
    .catch(error => {
        console.error('Error during claim submission:', error);
        alert('Error submitting claim, please try again.');
    });
}


// Function to add submit event listener for the form
function addSubmitEventListener() {
    // Ensure the form exists after showing it
    const finalSubmitForm = document.getElementById('finalSubmitForm');
    
    if (finalSubmitForm) {
        finalSubmitForm.addEventListener('submit', function(event) {
            submitClaim(event);  // Pass the event to submitClaim function
        });
    } else {
        console.error("Form element with ID 'finalSubmitForm' not found.");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Ensure that form submission listener is only added once the document is fully loaded
    const finalSubmitForm = document.getElementById('finalSubmitForm');
    if (finalSubmitForm) {
        finalSubmitForm.addEventListener('submit', function(event) {
            submitClaim(event);  // Pass the event to submitClaim function
        });
    }
});
