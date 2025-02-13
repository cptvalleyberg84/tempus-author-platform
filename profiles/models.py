from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


def profile_image_path(instance, filename):
    """
    Generate the upload path for profile images.
    This ensures consistent paths between development and production.
    """
    return f'profile_images/{filename}'


class UserProfile(models.Model):
    """
    User profile model for storing user-specific information.
    
    Maintains user's personal details, delivery information,
    and profile settings.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )

    postcode_validator = RegexValidator(
        regex=r'^[A-Za-z0-9]{4,6}$',
        message='Postcode must be 4-6 characters. Only letters and numbers'
    )
    profile_image = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        default='profile_images/default.jpg',
    )

    profile_bio = models.TextField(max_length=500, blank=True)

    profile_full_name = models.CharField(max_length=50, null=True, blank=True)

    profile_email = models.EmailField(max_length=254, null=True, blank=True)
    profile_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )

    profile_address1 = models.CharField(max_length=255, blank=True, null=True)
    profile_address2 = models.CharField(max_length=255, blank=True, null=True)
    profile_city = models.CharField(max_length=100, null=True, blank=True)

    profile_postcode = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        validators=[postcode_validator],
    )

    profile_country = CountryField(
        blank_label='Country', null=True, blank=True
    )

    profile_created = models.DateTimeField(auto_now_add=True)
    profile_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the UserProfile model.
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update user profile when User model is saved.
    
    Creates a new UserProfile instance for new users and ensures
    profile is saved for existing users.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
