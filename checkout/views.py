from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from works.models import Product
from .forms import OrderForm
from works.context_processors import bookcart_contents
import stripe


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bookcart = request.session.get('bookcart', {})

    if not bookcart:
        messages.error(request, "You ain't having no books in your bookcart.")
        return redirect(reverse('all_works'))

    current_bookcart = bookcart_contents(request)
    total = current_bookcart['total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    bookcart_items = []
    total = 0

    for item_id, quantity in bookcart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        bookcart_items.append({
            'product': product,
            'quantity': quantity,
        })

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing!')
    if not stripe_secret_key:
        messages.warning(request, 'Stripe secret key is missing!')

    context = {
        'order_form': order_form,
        'bookcart_items': bookcart_items,
        'total': total,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    template = 'checkout/checkout.html'
    return render(request, template, context)
