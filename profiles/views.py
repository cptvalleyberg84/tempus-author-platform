from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, PublicProfileForm
from checkout.models import Order
from blog.models import Comment


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    latest_comments = Comment.objects.filter(author=request.user)\
        .select_related('post')\
        .order_by('-created_on')[:3]

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    try:
        orders = profile.orders.all()
    except AttributeError:
        orders = []

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'form': form,
        'orders': orders,
        'latest_comments': latest_comments,
        'on_profile_page': True
    }

    return render(request, template, context)


def public_profile(request, user_id):
    """ Display public profile view """
    profile = get_object_or_404(UserProfile, user__id=user_id)

    if request.user.is_authenticated and request.user.id == user_id:
        return redirect('profile')

    form = PublicProfileForm(instance=profile)

    latest_comments = Comment.objects.filter(author=profile.user).select_related('post').order_by('-created_on')[:3]

    template = 'profiles/public_profile.html'
    context = {
        'profile': profile,
        'form': form,
        'latest_comments': latest_comments,
    }

    return render(request, template, context)


def order_history(request, order_id):
    """ A view to show individual order history """
    order = get_object_or_404(Order, id=order_id)

    messages.info(request, (
        f'This is a past confirmation for order number {order_id}. '
        'A confirmation email was sent on the order date.'
    ))

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'checkout/checkout_success.html', context)
