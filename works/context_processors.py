from decimal import Decimal
from django.shortcuts import get_object_or_404
from works.models import Product


def bookcart_contents(request):
    """
    Ensures that the book cart contents are available when rendering every page
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
            'title': book.name,
            'image': book.image,
            'category': book.category,
            'subtotal': Decimal(str(book.price * quantity))
        })

    context = {
        'bookcart': bookcart,
        'bookcart_items': bookcart_items,
        'total': total,
        'product_count': product_count,
    }

    return context
