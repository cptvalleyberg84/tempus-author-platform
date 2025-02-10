from django import forms
from .models import CarouselItem
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class CarouselItemAdminForm(forms.ModelForm):
    class Meta:
        model = CarouselItem
        fields = '__all__'

    def clean(self):
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
        image = self.cleaned_data.get('image')

        if image:
            try:
                w, h = get_image_dimensions(image)
                min_width = 1600
                min_height = 800

                if w != min_width or h != min_height:
                    raise ValidationError(
                        f'Image must be at least '
                        f'{min_width}x{min_height} '
                        'pixels. Your image is '
                        f'{w}x{h} pixels.'
                    )

                if image.size > 5 * 1024 * 1024:  # 5MB
                    raise ValidationError(
                        'Image keep filesize under 5MB.'
                    )

            except Exception:
                raise ValidationError(
                    'Please ensure the file is a valid image.'
                )

        return image
