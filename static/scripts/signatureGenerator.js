let claimNumber = '';
let generatedSignature = '';

function generateClaimNumber() {
    claimNumber = Math.floor(Math.random() * 1000000); 
    document.querySelector('#claimNumberDisplay').innerText = `Claim Number: ${claimNumber}`;
}

function generateSignature() {
    const claimDetails = document.querySelector('#claimDetails').value.trim(); 
    const claimerName = document.querySelector('#claimerName').value.trim(); 

    if (!claimDetails || !claimerName) {
        alert('Please fill in all fields to generate the signature.');
        return; 
    }

    if (!claimNumber) {
        generateClaimNumber();
    }

    const dataToSign = `${claimerName}:${claimDetails}:${claimNumber}`;
    generatedSignature = btoa(dataToSign); 

    localStorage.setItem('generatedSignature', generatedSignature);
    localStorage.setItem('claimNumber', claimNumber);
    localStorage.setItem('claimDetails', claimDetails);

    document.querySelector('#digitalSignature').innerText = `Generated Signature: ${generatedSignature}`;

    Swal.fire({
        title: 'Digital Signature Generated!',
        text: 'Do you want to copy the digital signature to the clipboard?',
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Yes, copy it!',
        cancelButtonText: 'No, thanks'
    }).then((result) => {
        if (result.isConfirmed) {
            navigator.clipboard.writeText(generatedSignature).then(() => {
                Swal.fire({
                    title: 'Signature copied to clipboard!',
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            }).catch(err => {
                Swal.fire({
                    title: 'Failed to copy signature!',
                    icon: 'error',
                    text: err.message,
                    confirmButtonText: 'Try again'
                });
            });
        }
    });
}
