from django import forms
from .models import CollaborationRequest


class CollaborationForm(forms.ModelForm):
    """
    Form for handling collaboration requests.

    This form provides a user interface for submitting collaboration requests.
    It includes custom styling for form fields and validation for name and
    message fields.
    """

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    subject = forms.CharField(
        label='Subject',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brief subject of your request'
        })
    )
    collaboration_type = forms.ChoiceField(
        label='Collaboration Type',
        choices=CollaborationRequest.COLLABORATION_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell me about your project or idea...',
            'rows': 4
        })
    )

    class Meta:
        """
        Meta class for CollaborationForm.

        Specifies the model to use and configures form fields and widgets.
        """
        model = CollaborationRequest
        fields = ['name', 'email', 'subject', 'collaboration_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your request'
            }),
            'collaboration_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell me about your project or idea...',
                'rows': 4
            })
        }

    def clean_name(self):
        """
        Custom validation for the name field.

        Ensures that the name field does not contain any numbers.

        Returns:
            str: The cleaned name value.

        Raises:
            ValidationError: If the name contains numbers.
        """
        name = self.cleaned_data.get('name', '').strip()
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name

    def clean_message(self):
        """
        Custom validation for the message field.

        Ensures that the message is at least 10 characters long.

        Returns:
            str: The cleaned message value.

        Raises:
            ValidationError: If the message is shorter than 10 characters.
        """
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Message must be at least 10 characters long."
            )
        return message
