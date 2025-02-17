from decimal import Decimal
from django.shortcuts import get_object_or_404
from works.models import Product


def bookcart_contents(request):
    """
    Context processor for book cart data.

    Makes book cart information available to all templates, including:
    - List of cart items with quantities and subtotals
    - Total price of all items
    - Total number of items in cart
    """
    bookcart = request.session.get('bookcart', {})

    total = Decimal('0.00')
    product_count = 0
    bookcart_items = []

    for item_id, quantity in bookcart.items():
        book = get_object_or_404(Product, pk=item_id)
        total += book.price * quantity
        product_count += quantity
        bookcart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'price': book.price,
            'product': book,
            'subtotal': Decimal(str(book.price * quantity))
        })

    context = {
        'bookcart': bookcart,
        'bookcart_items': bookcart_items,
        'total': total,
        'product_count': product_count,
    }

    return context
