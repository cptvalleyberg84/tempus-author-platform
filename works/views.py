from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from checkout.models import OrderItem
from .forms import ReviewForm


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
    reviews = work.reviews.filter(approved=True)
    review_form = ReviewForm()

    user_has_reviewed = False
    user_has_approved_review = False
    user_has_purchased = False

    if request.user.is_authenticated:
        user_review = work.reviews.filter(user=request.user).first()
        user_has_reviewed = user_review is not None
        user_has_approved_review = (
            user_review.approved if user_review else False
        )

    if request.user.is_authenticated:
        user_has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=work,
            order__payment_status='paid'
        ).exists()

    context = {
        'work': work,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
        'user_has_approved_review': user_has_approved_review,
        'user_has_purchased': user_has_purchased,
    }

    return render(request, 'works/work_detail.html', context)


def view_bookcart(request):
    """ A view that renders the book cart contents page """
    return render(request, 'works/bookcart.html')


def add_to_bookcart(request, work_id):
    """ Add a quantity of the specified product to the cart """
    work_id = str(work_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bookcart = request.session.get('bookcart', {})

    if work_id in list(bookcart.keys()):
        bookcart[work_id] += quantity
    else:
        bookcart[work_id] = quantity

    request.session['bookcart'] = bookcart
    return redirect(redirect_url)


def adjust_bookcart(request, work_id):
    """ Adjust the quantity of the specified product """

    quantity = int(request.POST.get('quantity'))
    bookcart = request.session.get('bookcart', {})

    if quantity > 0:
        bookcart[work_id] = quantity
    else:
        bookcart.pop(work_id)

    request.session['bookcart'] = bookcart
    return redirect(reverse('view_bookcart'))


def remove_from_bookcart(request, work_id):
    """ Remove the book from the book cart """

    try:
        bookcart = request.session.get('bookcart', {})
        bookcart.pop(str(work_id))
        request.session['bookcart'] = bookcart
        messages.success(request, 'Item removed from the bookcart')
        return redirect(reverse('view_bookcart'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


@login_required
def add_review(request, work_id):
    work = get_object_or_404(Product, id=work_id)

    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=work,
        order__payment_status='paid'
    ).exists()

    if not has_purchased:
        messages.error(
            request,
            'You can only review books that you have.'
        )
        return redirect('work_detail', work_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = work
            review.user = request.user
            review.save()
            messages.success(
                request, 'Review has been submitted for approval. Thank you!'
            )
    return redirect('work_detail', work_id)
