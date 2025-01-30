from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Either create profile automatically
        profile = UserProfile.objects.create(user=request.user)
        # Or redirect to profile creation page
        # return redirect('create_profile')

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
    }

    return render(request, template, context)
