from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_confirmation_email(order):
    """Send the user a confirmation email"""
    customer_email = order.email
    subject = f'Tempus Author Platform - Order Confirmation #{order.id}'

    # Get order items for the email
    order_items = order.orderitem_set.all()

    # Prepare context for email template
    context = {
        'order': order,
        'contact_email': settings.CONTACT_DISPLAY_EMAIL,
        'order_items': order_items,
    }

    # Render email body
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.html',
        context
    )

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error details
        print(f'Email error details: {str(e)}')
        raise  # Re-raise the exception to be handled by the view
