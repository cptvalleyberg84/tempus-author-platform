from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for submitting product reviews.

    Includes a star rating system and optional comment field.
    """
    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': (
                "Writing a review is optional, but your words can help others "
                "make better choices! Share your experience if you'd like."
            ),
            'rows': 4
        }),
        required=False
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
