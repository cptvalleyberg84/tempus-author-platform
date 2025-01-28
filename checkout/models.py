from django.db import models
from django.conf import settings


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'

    class Meta:
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('works.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )

    def __str__(self):
        return f"Order #{self.order.id} - Product: {self.product.name}"
