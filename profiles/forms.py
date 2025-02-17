from django import forms
from .models import UserProfile
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
import re


class UserProfileForm(forms.ModelForm):
    """
    Form for managing user profile information.

    Handles validation and cleaning of profile data including email,
    phone number, address details, and profile image.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def clean(self):
        """
        Validate that all required address fields are provided together.
        """
        cleaned_data = super().clean()
        address1 = cleaned_data.get('profile_address1')
        city = cleaned_data.get('profile_city')
        postcode = cleaned_data.get('profile_postcode')

        if any([address1, city, postcode]) and not all(
            [address1, city, postcode]
        ):
            raise ValidationError(
                'If providing address details, all fields (address, city, '
                'postcode) are required'
            )

        return cleaned_data

    def clean_profile_email(self):
        """
        Validate email domain is not a test/example domain.
        """
        email = self.cleaned_data.get('profile_email')
        if email:
            domain = email.split('@')[1]
            if domain in ['example.com', 'test.com']:
                raise ValidationError('Please use a valid email address')
        return email

    def clean_profile_postcode(self):
        """
        Validate postcode format.
        """
        postcode = self.cleaned_data.get('profile_postcode')
        if postcode:
            if not re.match(r'^[A-Za-z0-9]{4,6}$', postcode):
                raise forms.ValidationError(
                    'Postcode must be 4-6 characters and contain only letters'
                    ' and numbers'
                )
        return postcode

    def clean_profile_phone_number(self):
        """
        Validate phone number format.
        """
        phone = self.cleaned_data.get('profile_phone_number')
        if phone:
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError(
                    'Phone number must be entered in format: "+999999999"'
                )
        return phone

    def clean_profile_image(self):
        """
        Validate profile image size and dimensions.
        """
        image = self.cleaned_data.get('profile_image')

        if image:
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(
                    f'Image file is too large. Please keep filesize under '
                    f'{settings.MAX_UPLOAD_SIZE / (1024 * 1024)}MB.'
                )

            try:
                w, h = get_image_dimensions(image)
                if (w > settings.MAX_IMAGE_WIDTH or
                        h > settings.MAX_IMAGE_HEIGHT):
                    raise ValidationError(
                        f'Image dimensions cannot exceed '
                        f'{settings.MAX_IMAGE_WIDTH}x'
                        f'{settings.MAX_IMAGE_HEIGHT} '
                        'pixels. Your image is '
                        f'{w}x{h} pixels.'
                    )
            except Exception as e:
                raise ValidationError(
                    f'Unable to validate image dimensions: {str(e)}. '
                    f'Please ensure the file is a valid image.'
                )

        return image

    def __init__(self, *args, **kwargs):
        """
        Initialize form with custom placeholders and field settings.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'profile_full_name': 'Full Name',
            'profile_email': 'Email Address',
            'profile_phone_number': 'Phone Number',
            'profile_address1': 'Street Address',
            'profile_address2': 'Apartment, suite, etc. (optional)',
            'profile_city': 'City',
            'profile_postcode': 'Postal Code',
            'profile_country': 'Country',
            'profile_image': 'Profile Image',
            'profile_bio': 'Bio',
        }

        self.fields['profile_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = (
                'rounder-0 profile-form-input')
            self.fields[field].label = False


class PublicProfileForm(forms.ModelForm):
    """
    Form for displaying read-only public profile information.

    Shows limited profile fields with all inputs disabled.
    """
    class Meta:
        model = UserProfile
        fields = ('profile_image', 'profile_bio')

    def __init__(self, *args, **kwargs):
        """
        Initialize form with all fields set to read-only.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['disabled'] = True
