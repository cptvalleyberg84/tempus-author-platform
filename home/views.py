from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from works.models import Product


def index(request):
    """A view that displays the index page"""
    return render(request, 'home/index.html')


def search(request):
    """A view that displays the search results page"""
    query = request.GET.get('q', '')
    works = []

    if 'q' in request.GET:
        if not query:
            messages.warning(request, "You didn't enter any search criteria!")
        else:
            works = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

    context = {
        'works': works,
        'search_term': query,
    }

    return render(request, 'home/search_results.html', context)
