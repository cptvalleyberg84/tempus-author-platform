/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
document.addEventListener('DOMContentLoaded', function() {
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');


    // Handle real-time validation errors on the card element
    card.addEventListener('change', function(event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submission
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        $('#loading-overlay').fadeToggle(100);
        $('#payment-form').fadeToggle(100);
        card.update({ 'disabled': true});
        $('.submit-button').attr('disabled', true);
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
            }
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#loading-overlay').fadeToggle(100);
                $('#payment-form').fadeToggle(100);
                card.update({ 'disabled': false });
                $('.submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        }).catch(function(error) {
            console.error('Error:', error);
            $('#loading-overlay').fadeToggle(100);
            $('#payment-form').fadeToggle(100);
            card.update({ 'disabled': false });
            $('.submit-button').attr('disabled', false);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const postcodeInput = document.getElementById('id_billing_postcode');
    if (postcodeInput) {
        postcodeInput.addEventListener('input', function(e) {
            const postcode = e.target.value;
            const postcodeRegex = /^[A-Za-z0-9]{4,6}$/;
            const errorDiv = document.getElementById('postcode-error');
            const submitButton = document.getElementById('submit-button');
            
            if (!postcodeRegex.test(postcode)) {
                if (!errorDiv) {
                    const div = document.createElement('div');
                    div.id = 'postcode-error';
                    div.className = 'invalid-feedback d-block';
                    div.textContent = 'Postcode must be 4-6 characters and contain only letters and numbers';
                    e.target.classList.add('is-invalid');
                    e.target.parentNode.appendChild(div);
                }
                submitButton.disabled = true;
            } else {
                if (errorDiv) {
                    errorDiv.remove();
                }
                e.target.classList.remove('is-invalid');
                submitButton.disabled = false;
            }
        });
    }
});