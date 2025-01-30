from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


# Create your models here.
class UserProfile(models.Model):
    """
    A user profile model for maintaining default delivery
    information, order history, and recent activity
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    postcode_validator = RegexValidator(
        regex=r'^[A-Za-z0-9]{4,6}$',
        message='Postcode must be 4-6 characters. Only letters and numbers'
    )
    # Profile specific fields
    profile_image = models.ImageField(
        upload_to='profile_images',
        null=True,
        blank=True,
        default='profile_images/default.jpg',
    )

    profile_bio = models.TextField(max_length=500, blank=True)

    # Default adress information
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
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
