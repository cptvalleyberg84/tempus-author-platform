from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def all_works(request):
    """A view that displays All the Products in the Works page"""
    works = Product.objects.all()
    categories = Category.objects.all()
    current_category = None

    if 'category' in request.GET:
        category_name = request.GET['category']
        works = works.filter(category__name=category_name)
        current_category = category_name

    context = {
        'works': works,
        'categories': categories,
        'current_category': current_category
    }

    return render(request, 'works/works.html', context)


def work_detail(request, work_id):
    """ A view to show individual work details """

    work = get_object_or_404(Product, pk=work_id)

    context = {
        'work': work,
    }

    return render(request, 'works/work_detail.html', context)


def view_book_cart(request):
    """ A view that renders the book cart contents page """
    return render(request, 'works/book_cart.html')
