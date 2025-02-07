from django import forms
from .models import CarouselItem


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
