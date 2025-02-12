from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from checkout.models import OrderItem
from .forms import ReviewForm


def all_works(request):
    """
    Display all products/works with optional category filtering.
    """
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
    """
    Display detailed information about a specific work.

    Shows work details, approved reviews, and handles user-specific
    display logic for reviews and purchases.
    """
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
    """
    Display the contents of the user's book cart.
    """
    return render(request, 'works/bookcart.html')


def add_to_bookcart(request, work_id):
    """
    Add a specified quantity of a work to the book cart.
    """
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
    """
    Adjust the quantity of a work in the book cart.

    If quantity is set to 0, the item is removed from the cart.
    """
    quantity = int(request.POST.get('quantity'))
    bookcart = request.session.get('bookcart', {})

    if quantity > 0:
        bookcart[work_id] = quantity
    else:
        bookcart.pop(work_id)

    request.session['bookcart'] = bookcart
    return redirect(reverse('view_bookcart'))


def remove_from_bookcart(request, work_id):
    """
    Remove a work from the book cart.
    Handles cases where the item might not exist in the cart.
    """
    try:
        bookcart = request.session.get('bookcart', {})
        work_id = str(work_id)

        if work_id in bookcart:
            bookcart.pop(work_id)
            request.session['bookcart'] = bookcart
            messages.success(request, 'Item removed from the bookcart')
        else:
            messages.info(request, 'This item was not in your bookcart')

        return redirect(reverse('view_bookcart'))

    except Exception as e:
        messages.error(request, f'Error removing item from bookcart: {e}')
        return redirect(reverse('view_bookcart'))


@login_required
def add_review(request, work_id):
    """
    Add a review for a purchased work.

    Only allows reviews from users who have purchased the work.
    Reviews require approval before being displayed.
    """
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
