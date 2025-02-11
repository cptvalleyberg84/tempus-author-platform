from django.db import models
from django.conf import settings
from django.db.models import Sum, F
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from profiles.models import UserProfile


class Order(models.Model):

    user_profile = models.ForeignKey(
        UserProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_orders'
    )

    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    order_date = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(max_length=254)
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    postcode_validator = RegexValidator(
        regex=r'^[A-Za-z0-9]{4,6}$',
        message=(
            'Postcode must be 4-6 characters and contain only letters and '
            'numbers'
        )
    )

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    billing_address1 = models.CharField(max_length=255)
    billing_address2 = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=100, null=False, blank=False)
    billing_postcode = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        validators=[postcode_validator],
        help_text='Enter a 4-6 characrters of postcode.'
    )
    billing_country = CountryField(
        blank_label='Country *', null=False, blank=False
    )

    def update_total(self):
        """Calculate and update the total amount from all order items"""
        total = self.orderitem_set.aggregate(
            total=Sum(F('quantity') * F('price')) or 0
        )['total'] or 0
        self.total_amount = total
        self.save()

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'

    class Meta:
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'works.Product',
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically set the price
        from the product
        """
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} "
            f"on order {self.order.id}"
        )
