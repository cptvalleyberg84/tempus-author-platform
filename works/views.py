from django.shortcuts import render, get_object_or_404
from .models import Product


def all_works(request):
    """A view that displays All the Products in the Works page"""
    works = Product.objects.all()
    categories = None

    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        works = works.filter(category__name__in=categories)

    context = {
        'works': works,
    }

    return render(request, 'works/works.html', context)


def work_detail(request, work_id):
    """ A view to show individual work details """

    work = get_object_or_404(Product, pk=work_id)

    context = {
        'work': work,
    }

    return render(request, 'works/work_detail.html', context)
