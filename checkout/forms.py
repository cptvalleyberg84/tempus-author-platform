import re
from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'billing_address1',
            'billing_address2',
            'billing_city',
            'billing_postcode',
            'billing_country',
        )

    def clean_billing_postcode(self):
        postcode = self.cleaned_data.get('billing_postcode')
        if not re.match(r'^[A-Za-z0-9]{4,6}$', postcode):
            raise forms.ValidationError(
                'Postcode must be 4-6 characters and contain only letters and '
                'numbers'
            )
        return postcode

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'billing_address1': 'Street Address',
            'billing_address2': 'Apartment, suite, etc. (optional)',
            'billing_city': 'City',
            'billing_postcode': 'Postal Code',
            'billing_country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            })
        }
