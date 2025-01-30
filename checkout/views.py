from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from works.models import Product
from .models import OrderItem, Order
from .forms import OrderForm
from works.context_processors import bookcart_contents
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bookcart = request.session.get('bookcart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'billing_address1': request.POST['billing_address1'],
            'billing_address2': request.POST['billing_address2'],
            'billing_city': request.POST['billing_city'],
            'billing_postcode': request.POST['billing_postcode'],
            'billing_country': request.POST['billing_country'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()

            for item_id, quantity in bookcart.items():
                try:
                    product = Product.objects.get(pk=item_id)
                    if isinstance(quantity, list):
                        quantity = sum(quantity)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                except Product.DoesNotExist:
                    messages.error(request, (
                        "Something not found."
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Calculate total
            total = sum(
                item.product.price * item.quantity
                for item in order.orderitem_set.all()
            )
            print(f"Calculated total: {total}")
            order.total = total
            order.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.id]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bookcart = request.session.get('bookcart', {})
        if not bookcart:
            messages.error(request,
                           "You ain't having no books in your bookcart.")
            return redirect(reverse('all_works'))

        current_bookcart = bookcart_contents(request)
        total = current_bookcart['total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing!')
    if not stripe_secret_key:
        messages.warning(request, 'Stripe secret key is missing!')

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bookcart_items': current_bookcart['bookcart_items'],
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, id=order_id)
    total = sum(
        item.product.price * item.quantity
        for item in order.orderitem_set.all()
    )

    if 'bookcart' in request.session:
        del request.session['bookcart']

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_id}. A confirmation \
        email will be sent to {order.email}.')

    context = {
        'order': order,
        'total': total,
    }

    return render(request, 'checkout/checkout_success.html', context)
