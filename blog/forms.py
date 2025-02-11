from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing blog post comments.
    """

    class Meta:
        """
        Meta class for CommentForm.
        """
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
