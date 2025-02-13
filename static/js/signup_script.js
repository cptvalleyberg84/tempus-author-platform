document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.querySelector('form[action*="account_signup"]');
    const newsletterCheckbox = document.getElementById('newsletterSignup');
    
    if (signupForm && newsletterCheckbox) {
        const googleScriptUrl = newsletterCheckbox.dataset.formUrl;
        
        signupForm.addEventListener('submit', async function(e) {
            if (newsletterCheckbox.checked) {
                const emailInput = document.querySelector('input[type="email"]');
                if (emailInput && emailInput.value) {
                    // Send to Google Script
                    const formData = new FormData();
                    formData.append('email', emailInput.value);
                    formData.append('source', 'signup_form');
                    
                    // Use fetch to send the data
                    fetch(googleScriptUrl, {
                        method: 'POST',
                        body: formData
                    }).catch(console.error);
                }
            }
        });
    }
});