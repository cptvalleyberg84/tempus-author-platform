from django import forms
from .models import CarouselItem
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class CarouselItemAdminForm(forms.ModelForm):
    """
    Form for managing carousel items in the admin interface.
    """
    class Meta:
        model = CarouselItem
        fields = '__all__'

    def clean(self):
        """
        Validate that the appropriate link type is provided'
        ' based on the selected style.
        """
        cleaned_data = super().clean()
        style = cleaned_data.get('style')
        product = cleaned_data.get('product')
        blog_post = cleaned_data.get('blog_post')
        external_link = cleaned_data.get('external_link')

        if style == 'product' and not product:
            raise forms.ValidationError(
                "For Product style, please select a Product."
            )
        elif style == 'blog' and not blog_post:
            raise forms.ValidationError(
                "For Blog style, please select a Blog Post."
            )
        elif style == 'external' and not external_link:
            raise forms.ValidationError(
                "For External style, please provide an External Link."
            )

        return cleaned_data

    def clean_image(self):
        """
        Validate image dimensions and file size for carousel items.
        """
        image = self.cleaned_data.get('image')

        if image:
            try:
                # Check if it's a valid image file
                w, h = get_image_dimensions(image)

                if not w or not h:
                    raise ValidationError(
                        'Could not read image dimensions.'
                        ' Please ensure the file is a valid image.'
                    )

                # Minimum dimensions
                min_width = 800
                min_height = 400

                if w < min_width or h < min_height:
                    raise ValidationError(
                        f'Image must be at least {min_width}x{min_height} px. '
                        f'Your image is {w}x{h} pixels. '
                    )

                # Maximum file size (5MB)
                if image.size > 5 * 1024 * 1024:
                    raise ValidationError(
                        'Image file size must be under 5MB. '
                        'Please compress your image.'
                    )

            except Exception as e:
                if 'image dimensions' in str(e):
                    raise ValidationError(
                        'Could not read image dimensions. Please ensure'
                        ' the file is a valid image format '
                        '(JPEG, PNG, GIF).'
                    )
                else:
                    raise ValidationError(
                        'Please ensure the file is a valid image in JPEG, '
                        'PNG, or GIF format.'
                    )

        return image
