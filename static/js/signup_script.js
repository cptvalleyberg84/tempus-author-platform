document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.querySelector('form[action="/accounts/signup/"]');
    const newsletterCheckbox = document.getElementById('newsletterSignup');
    const emailInput = document.getElementById('id_email');
    const nameInput = document.getElementById('id_username');

    if (!signupForm || !newsletterCheckbox || !emailInput) {
        return;
    }

    signupForm.addEventListener('submit', async function(e) {
        if (newsletterCheckbox.checked) {
            e.preventDefault();
            
            try {
                const googleScriptUrl = newsletterCheckbox.dataset.formUrl;
                if (!googleScriptUrl) {
                    throw new Error('Google Script URL not found');
                }

                const formData = new URLSearchParams();
                formData.append('Date', new Date().toISOString());
                formData.append('Email', emailInput.value);
                formData.append('Name', nameInput ? nameInput.value : '');

                const response = await fetch(googleScriptUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json'
                    },
                    body: formData
                });

                const responseData = await response.json();
                if (!response.ok) {
                    throw new Error('Newsletter subscription failed');
                }
            } catch (error) {
                console.error('Newsletter subscription failed:', error);
            }

            // Submit the form programmatically to continue with Django signup
            signupForm.submit();
        }
    });
});