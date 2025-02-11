from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from works.models import Product
from blog.models import Post
from .models import CarouselItem


def index(request):
    """
    Display the index page.
    """
    return render(request, 'home/index.html')


def search(request):
    """
    Display search results for works and blog posts.
    """
    query = request.GET.get('q', '')
    works = []
    blog_posts = []

    if 'q' in request.GET:
        if not query:
            messages.warning(request, "You didn't enter any search criteria!")
        else:
            works = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

            blog_posts = Post.objects.filter(
                Q(post_title__icontains=query) |
                Q(post_content__icontains=query),
                post_status=1
            ).distinct()

    total_results = len(works) + len(blog_posts)

    context = {
        'works': works,
        'blog_posts': blog_posts,
        'search_term': query,
        'total_results': total_results,
    }

    return render(request, 'home/search_results.html', context)


def home(request):
    """
    Display the home page with carousel items and latest content.
    """
    carousel_items = CarouselItem.objects.filter(
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__isnull=False,
        end_date__lt=timezone.now()
    ).order_by('order')

    latest_post = Post.objects.filter(post_status=1)\
        .order_by('-post_created_on').first()
    latest_product = Product.objects.order_by('-created_date').first()

    context = {
        'carousel_items': carousel_items,
        'latest_post': latest_post,
        'latest_product': latest_product,
    }
    return render(request, 'home/index.html', context)
