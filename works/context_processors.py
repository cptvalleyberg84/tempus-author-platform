from decimal import Decimal


def bookcart_contents(request):
    """
    Ensures that the book cart contents are available when rendering every page
    """
    bookcart = request.session.get('bookcart', {})

    total = Decimal('0.00')
    product_count = 0
    cart_items = []

    for item_id, item_data in bookcart.items():
        total += Decimal(str(item_data['price'])) * item_data['quantity']
        product_count += item_data['quantity']
        cart_items.append({
            'item_id': item_id,
            'quantity': item_data['quantity'],
            'price': item_data['price'],
            'format': item_data['format'],
            'title': item_data['title'],
            'subtotal': Decimal(str(item_data['price']))*item_data['quantity']
        })

    context = {
        'bookcart': bookcart,
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }

    return context
