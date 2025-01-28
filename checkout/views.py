from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from works.models import Product
from .forms import OrderForm


def checkout(request):
    bookcart = request.session.get('bookcart', {})

    if not bookcart:
        messages.error(request, "You ain't having no books in your bookcart.")
        return redirect(reverse('all_works'))

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

    context = {
        'order_form': order_form,
        'bookcart_items': bookcart_items,
        'total': total,
    }

    template = 'checkout/checkout.html'
    return render(request, template, context)
