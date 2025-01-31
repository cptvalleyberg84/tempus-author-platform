from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_confirmation_email(order):
    """Send the user a confirmation email"""
    customer_email = order.email
    subject = f'Order Confirmation - Order Number {order.id}'

    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.html',
        {'order': order, 'contact_email': settings.CONTACT_DISPLAY_EMAIL}
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )
    except Exception as e:
        print(f'An error occurred: {e}')
